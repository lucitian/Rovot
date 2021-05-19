from django.urls import path
from . import views
from .views import ChatterBotApiView
from django.conf.urls import url

urlpatterns = [
    path('', views.title, name='rovot-title'),
    path('register/', views.register, name='rovot-register'),
    path('login/', views.auth_login, name='rovot-login'),
    path('logout/', views.auth_logout, name="rovot-logout"),

    path('rovot/', views.home, name='rovot-home'),
    url(r'^api/chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
]