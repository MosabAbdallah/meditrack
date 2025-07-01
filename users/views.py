from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_user(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('register')
        User.objects.create_user(request.POST)
        return redirect('login')
    return render(request, 'users/register.html')

def login(request):
    if request.method == 'POST':
        user = User.objects.authenticate(
            request.POST['email'],
            request.POST['password']
        )
        if user:
            request.session['user_id'] = user.id
            return redirect('/patients/')
        messages.error(request, "Invalid email or password")
        return redirect('login')
    return render(request, 'users/login.html')

def logout(request):
    if request.method == 'POST':
        request.session.flush()
        return render(request, 'users/logout.html')  
    return render(request, 'users/confirm_logout.html')  


def about_page(request):
    return render(request, 'users/about.html')

def home_page(request):
    return render(request, 'users/home.html')
