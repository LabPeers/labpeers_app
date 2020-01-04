# accounts/urls.py
from django.urls import path
#from django.contrib.auth.views import ( password_reset_done, password_reset_confirm, password_reset_complete)
#from django.contrib.auth.views import PasswordResetView


from . import views


urlpatterns = [
    path('accounts/signup/', views.SignUp, name='signup'),
# =============================================================================
    path('accounts/logout/', views.logout_request, name='logout'),
    #path('accounts/reset-password/',PasswordResetView.as_view(), name='reset_password'),
    #path('accounts/reset-password/done/', password_reset_done, name='password_reset_done'),
    #path('accounts/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm, name='password_reset_confirm'),
    #path('accounts/reset-password/complete/', password_reset_complete,{'template_name': 'accounts/reset_password_complete.html'}, name='password_reset_complete'),



#     path('accounts/login/', views.login_request, name="login"),
# ]
# =============================================================================
]