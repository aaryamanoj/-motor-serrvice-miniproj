from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from datetime import datetime
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    return render(request, 'home.html')
def service(request):
    return render(request, 'service.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')




def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValidationError("Username must be 3-20 characters long and contain only letters, numbers, and underscores.")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    
from .models import Appointment

def appointment_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        state = request.POST.get('state')
        city = request.POST.get('city')
        location_type = request.POST.get('location_type')
        address = request.POST.get('address')

        if not all([name, phone, service, state, city, location_type]):
            messages.error(request, 'All fields are required for booking an appointment.')
            return render(request, 'appointment.html')
        
        try:
            if location_type == 'address' and not address:
                raise ValidationError("Address is required when 'Use Address' is selected.")
            
            # Save the appointment to the database
            appointment = Appointment(
                name=name,
                phone=phone,
                service=service,
                state=state,
                city=city,
                location_type=location_type,
                address=address if location_type == 'address' else None
            )
            appointment.save()
            
            return redirect('appointment_success')
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    return render(request, 'appointment.html')

def appointment_success_view(request):
    return render(request, 'appointment_success.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'New contact form submission: {subject}',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,
            ['aryamanoj970@gmail.com'],  # Replace with your email
            fail_silently=False,
        )
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact_success')
    
    return render(request, 'contact.html')

def contact_success(request):
    return render(request, 'contact_success.html')



# serviceapp/views.py

from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

