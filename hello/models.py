from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
# =============================================================================
# class Greeting(models.Model):
#       when = models.DateTimeField("date created", auto_now_add=True)
#             
# =============================================================================
 
class Graph_Data(models.Model):
        graph_title = models.CharField(max_length=500)
#        myX = ArrayField(models.FloatField())
        myX = models.CharField(max_length=500)
        user = models.ForeignKey(User)

       
        
# =============================================================================
#       r = models.FloatField()
#       x = models.FloatField(default=0)
# =============================================================================