from django.contrib import admin
from django.urls import path, include

admin.autodiscover()


from tracking.views import TrackView
from tracking.views import EditTrackView

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/


urlpatterns = [
    path("track/", TrackView.as_view(), name='track'),
    path("track/<int:pk>", EditTrackView.as_view(), name='track_project'),
]
