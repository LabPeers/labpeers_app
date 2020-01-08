from django.db import models
from djanog.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User)
    image=models.ImageField(upload_to='profile_image',blank=True)