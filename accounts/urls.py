# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('accounts/signup/', views.SignUp, name='signup'),
]