from django.urls import path
from . import views
from .views import appointment_view, appointment_success_view 

urlpatterns = [
    path('', views.home, name='home'),
    path('service/', views.service, name='service'),
    path('about/', views.about, name='about'),
    
    path('register/', views.register, name='register'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('appointment/success/', views.appointment_success_view, name='appointment_success'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('login/', views.login, name='login'),
]