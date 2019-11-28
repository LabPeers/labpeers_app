from django.contrib import admin
from django.urls import path, include

admin.autodiscover()

from hello.views import HomeView
from hello.views import HomeReal
from hello.views import Register
from hello.views import Profile



# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls')), # new
    #path("hello/", include('gettingstarted.urls')),
    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/profile/",Profile.as_view(), name='profile'),
    path("", HomeReal.as_view(), name='home'),
    path("bubblechart/", HomeView.as_view(), name='bubblechart'),
    path("register/", Register.as_view(), name='register'),
 #   path("db/", hello.views.db, name="db"),
]
