from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

# Create your views here.
def login(request):
    return render(request, 'directories/login.html')

def register(request):
    ctx = {
            'form': None
    }

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            uname = form.cleaned_data.get('username')

    else:
        form = UserRegistrationForm()

    ctx['form'] = form

    return render(request, 'directories/register.html', ctx)

def home(request):
    return render(request, 'directories/home.html')