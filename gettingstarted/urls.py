from django.contrib import admin
from django.urls import path, include

admin.autodiscover()


from mybubble.views import HomeView
from mybubble.views import HomeReal
#from hello.views import Register
from mybubble.views import Profile
from mybubble.views import Projects
from mybubble.views import EditView
from mybubble.views import DeleteView
from mybubble.views import GalleryView
from mybubble.views import DeletePlotView
from mybubble.views import SecretFileView
from mybubble.views import MyTestView
from myscatter.views import TrackView, EditTrackView, TrackingProjects, TrackingDeleteView


#from hello.views import HomeView_details
#from accounts.views import SignUp
#from . import views


#To be able to run app locally
from django.conf import settings
from django.views.static import serve



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
    path("accounts/test/",MyTestView.as_view(), name='test'),
    path("accounts/profile/profile_pics/", SecretFileView.as_view(), name='profile_pics'),
    path("", HomeReal.as_view(), name='home'),
    path("bubblechart/", HomeView.as_view(), name='bubblechart'),
    #path("bubblechart/<int:pk>", EditView.as_view(), name='bubblechart_project'),
    path("bubblechart/<safekey>", EditView.as_view(), name='bubblechart_project'),
    path("projects/", Projects.as_view(), name='projects'),
    path("projects/<safekey>", DeleteView.as_view(), name='projects_delete'),
    path("tracking_projects/", TrackingProjects.as_view(), name='tracking_projects'),
    path("tracking_projects/<safekey>", TrackingDeleteView.as_view(), name='projects_delete'),
    path("gallery/", GalleryView.as_view(), name='gallery'),
    path("gallery/<int:pk>", DeletePlotView.as_view(), name='plot_delete'),
    path("track/", TrackView.as_view(), name='track'),
    #path("track/<int:pk>", EditTrackView.as_view(), name='track_project'),
    path("track/<safekey>", EditTrackView.as_view(), name='track_project'),
 #   path('bubblechart/<graph_filename>/', HomeView_details.as_view(), name='your_project'),
 #   path("accounts/signup/", views.SignUp, name='signup'),
 #   path("db/", hello.views.db, name="db"),
]


#To be able to run app locally

#if settings.DEBUG:
#    urlpatterns += [
#        path(r'^media/(?P<path>.*)$', serve, {
#            'document_root': settings.MEDIA_ROOT,
#        }),
#    ]

