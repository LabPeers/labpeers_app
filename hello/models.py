from django.db import models
from django.forms import ModelForm

# Create your models here.
class Greeting(models.Model):
     when = models.DateTimeField("date created", auto_now_add=True)

# =============================================================================
# class Input(models.Model):
#     r = models.FloatField()
# 
# class InputForm(ModelForm):
#     class Meta:
#         model = Input
#         fields = "__all__"
# =============================================================================
