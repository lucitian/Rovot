from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'directories/login.html')

def register(request):
    return render(request, 'directories/register.html')

def home(request):
    return render(request, 'directories/home.html')