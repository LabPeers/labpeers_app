# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate


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
            login(request, user)
    
    
    
    form = UserCreationForm
    return render(request, 'signup.html', {"form":form})