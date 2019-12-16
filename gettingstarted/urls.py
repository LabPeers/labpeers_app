from django.contrib import admin
from django.urls import path, include

admin.autodiscover()

from bubble.views import HomeView
from bubble.views import HomeReal
#from hello.views import Register
from bubble.views import Profile
#from hello.views import HomeView_details
#from accounts.views import SignUp
#from . import views



# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('accounts.urls')), # new
    #path("hello/", include('gettingstarted.urls')),
    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/profile/",Profile.as_view(), name='profile'),
    path("", HomeReal.as_view(), name='home'),
    path("bubblechart/", HomeView.as_view(), name='bubblechart'),
 #   path('bubblechart/<graph_filename>/', HomeView_details.as_view(), name='your_project'),
 #   path("accounts/signup/", views.SignUp, name='signup'),
 #   path("db/", hello.views.db, name="db"),
]
