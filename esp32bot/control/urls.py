from django.urls import path
from . import views
from .views import create_record, read_records
urlpatterns = [
    #  path("", home_page_view, name="home"),
    path('create/', create_record, name='create_record'),
    path('read/', read_records, name='read_records'),
    path('', views.control_pin, name='control_pin'),
    path('check-connection/', views.check_connection, name='check_connection'),
    path('set-ip/', views.set_ip, name='set_ip'),
]