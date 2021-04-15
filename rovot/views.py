from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login(request):
    ctx = {
            'form': None
    }
    
    if request.method == 'POST':
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            '''login(request, user)'''
            messages.success(request, 'Login successful!')

            return redirect('rovot-home')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'directories/login.html', ctx)

def register(request):
    ctx = {
            'form': None
    }

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            
            uname = form.cleaned_data.get('username')
            messages.success(request, f"Success! An account was created for {uname}!")

            return redirect('rovot-login')

    else:
        form = UserRegistrationForm()

    ctx['form'] = form

    return render(request, 'directories/register.html', ctx)

def home(request):
    return render(request, 'directories/home.html')