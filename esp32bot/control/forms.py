from django import forms

class IPAddressForm(forms.Form):
    ipaddress = forms.GenericIPAddressField(protocol='both', required=True, label='ESP32 IP Address')
