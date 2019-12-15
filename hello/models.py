from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

#Import so you can associate user and their data
from django.conf import settings

# Create your models here.
# =============================================================================
# class Greeting(models.Model):
#       when = models.DateTimeField("date created", auto_now_add=True)
#             
# =============================================================================
 
class Graph_Data(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, 
                                 on_delete=models.CASCADE)
        graph_filename=models.CharField(default='Your_file_name',max_length=500)
        graph_title = models.CharField(default='Your graph title',max_length=500)
        graph_xlabel = models.CharField(default='x-axis label',max_length=500)
        graph_ylabel = models.CharField(default='y-axis label',max_length=500)
#        myX = ArrayField(models.FloatField())
        myX = models.CharField(max_length=500)
        myY = models.CharField(max_length=500)
        myRadius = models.CharField(max_length=500)

        #user = models.ForeignKey(User)

       
        
# =============================================================================
#       r = models.FloatField()
#       x = models.FloatField(default=0)
# =============================================================================