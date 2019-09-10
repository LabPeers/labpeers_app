from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

from hello.views import HomeView

import hello.views


# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/


urlpatterns = [
    path("", HomeView.as_view(), name='home'),
 #   path("db/", hello.views.db, name="db"),
 #   path("admin/", admin.site.urls),
]
