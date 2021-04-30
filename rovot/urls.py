from django.urls import path
from . import views

urlpatterns = [
    path('', views.title, name='rovot-title'),
    path('login/', views.auth_login, name='rovot-login'),
    path('register/', views.register, name='rovot-register'),
    path('rovot/', views.home, name='rovot-home')
]