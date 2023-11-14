from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    # check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login user
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again'))
            return redirect('home')
    
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('home')

def register_user(request):
    return render(request, 'register.html', {})



