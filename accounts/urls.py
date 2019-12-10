# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('accounts/signup/', views.SignUp, name='signup'),
# =============================================================================
#   path('accounts/logout/', views.logout_request, name='logout'),
#     path('accounts/login/', views.login_request, name="login"),
# ]
# =============================================================================
]