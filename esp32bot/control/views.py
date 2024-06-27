from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import ESP32Record
from django.views.decorators.csrf import csrf_exempt
import json ,requests
from django.utils import timezone
from .forms import IPAddressForm

# def home_page_view(request):
#     return render(request, 'control/index.html')

@csrf_exempt
def create_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ip_address = data.get('ip_address')
        if ip_address:
            record = ESP32Record(ip_address=ip_address)
            record.save()
            return JsonResponse({'status': 'success', 'id': record.id}, status=201)
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    return HttpResponse(status=405)

def read_records(request):
    records = ESP32Record.objects.all().values('id', 'ip_address','timestamp')
    return JsonResponse(list(records), safe=False)


def control_pin(request):
    if 'esp32_ip' not in request.session:
        return redirect('set_ip')

    ESP32_IP = f"http://{request.session['esp32_ip']}/control"
    
    if request.method == 'POST':
        pins = request.POST.getlist('pins[]')
        state = request.POST.get('state')
        payload = {'pins': ','.join(pins), 'state': state}
        try:
            response = requests.get(ESP32_IP, params=payload)
            return JsonResponse({'status': 'success', 'message': response.text})
        except requests.RequestException as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'control/index.html')

def check_connection(request):
    if 'esp32_ip' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'ESP32 IP not set'})

    ESP32_IP = f"http://{request.session['esp32_ip']}/control"
    
    try:
        response = requests.get(ESP32_IP)
        return JsonResponse({'status': 'connected', 'message': 'connected ','ipaddr': request.session['esp32_ip']})
    except requests.RequestException:
        # Send a command to set specific pins to low
        set_pins_to_low(request)
        return JsonResponse({'status': 'disconnected', 'message': 'disconnected'})

def set_pins_to_low(request):
    if 'esp32_ip' not in request.session:
        return
    
    ESP32_IP = f"http://{request.session['esp32_ip']}/control"
    pins = ['26', '25', '32', '33']
    payload = {'pins': ','.join(pins), 'state': 'low'}
    try:
        requests.get(ESP32_IP, params=payload)
    except requests.RequestException:
        pass  # Ignore any errors here as the device is already disconnected

def set_ip(request):
    if request.method == 'POST':
        form = IPAddressForm(request.POST)
        if form.is_valid():
            request.session['esp32_ip'] = form.cleaned_data['ipaddress']
            return redirect('control_pin')
    else:
        form = IPAddressForm()
    return render(request, 'control/set_ip.html', {'form': form})
