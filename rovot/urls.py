from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='rovot-login'),
    path('register/', views.register, name='rovot-register'),
    path('rovot/', views.home, name='rovot-home')
]