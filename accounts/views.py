# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages


# =============================================================================
# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     #success_url = '/accounts/login/'
#     template_name = 'signup.html'
# =============================================================================


def SignUp(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:form.error_messages[msg]")
                
    form = UserCreationForm
    return render(request, 'signup.html', {"form":form})




# =============================================================================
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")
# =============================================================================

    
    

