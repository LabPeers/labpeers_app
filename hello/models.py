from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import ModelForm

# Create your models here.
class Greeting(models.Model):
      when = models.DateTimeField("date created", auto_now_add=True)
            
 
class User_title(models.Model):
#        p = ArrayField(models.CharField(max_length=3, blank=True))
        user_title = models.CharField(max_length=500)
#        myX = ArrayField(models.IntegerField())

        
        
# =============================================================================
#       r = models.FloatField()
#       x = models.FloatField(default=0)
# =============================================================================



