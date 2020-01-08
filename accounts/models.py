from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    #user=models.OneToOneField(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_image', blank=True, null=True)
    