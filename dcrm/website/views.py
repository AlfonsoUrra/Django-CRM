from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Cliente

def home(request):
    records = Cliente.objects.all()
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
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            # login user
            login(request, user)
            messages.success(request, ('You have registered...'))
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        custumer_record = Cliente.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': custumer_record})
    else:
        messages.success(request, ('Please login to view customer record'))
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Cliente.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Customer Record has been deleted'))
        return redirect('home')
    else:
        messages.success(request, ('Please login to delete customer record'))
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home   ')
        return render(request, 'add_record.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Cliente.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, ('Record has been updated'))
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, ('Please login to update customer record'))
        return redirect('home')




