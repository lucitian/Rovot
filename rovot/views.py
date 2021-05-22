import json, pickle
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.views.generic import View
from django.http import JsonResponse

from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import sys
from . import text_processing

from .LogisticRegression import LogisticRegression

sys.modules['text_processing'] = text_processing

model = pickle.load(open('rovot/model.sav', 'rb'))

# Create your views here.
def title(request):
    return render(request, 'directories/title.html')

def register(request):
    ctx = {
            'form': None
    }

    if request.user.is_authenticated:
        return redirect('rovot-home')
    else: 
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

def auth_login(request):
    ctx = {
            'form': None
    }
    
    if request.user.is_authenticated:
        return redirect('rovot-home')
    else: 
        if request.method == 'POST':
            username = request.POST.get('login-username')
            password = request.POST.get('login-password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')

                return redirect('rovot-home')
            else:
                messages.info(request, 'Username or password is incorrect')

        return render(request, 'directories/login.html', ctx)

def auth_logout(request):
    logout(request)
    return redirect('rovot-login')

@login_required(login_url='rovot-login')
def home(request):
    return render(request, 'directories/home.html')

class ChatterBotApiView(View):

    chatterbot = ChatBot(**settings.CHATTERBOT)

    trainer = ChatterBotCorpusTrainer(chatterbot)

    """
    trainer.train(
        "chatterbot.corpus.english.ai",
        "chatterbot.corpus.english.conversations"
    )       
    """
    
    def post(self, request, *args, **kwargs):

        input_data = json.loads(request.read().decode('utf-8'))

        lbl = ('fear', 'sadness', 'anger', 'love', 'joy', 'surprise')

        prediction = model.predict(input_data['text'])

        confidence = prediction[1]

        print(f"Text: {input_data['text']}\nPrediction: {lbl[int(prediction[0][0])]} | Confidence: {confidence[0][int(prediction[0][0])] * 100:.2f}%\n")

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):

        return JsonResponse({
            'name': self.chatterbot.name
        })
     