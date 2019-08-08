#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:00:53 2019

@author: egetenmeyer
"""
from django.contrib.postgres.fields import ArrayField
from django import forms
from .models import User_title
from django.db import models


class HomeForm(forms.ModelForm):
    user_title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter the plot title here...'
        }
    ))
    
    #myX = ArrayField(models.IntegerField())
    

    class Meta:
        model = User_title
        #fields = ('post','myX',)
#        fields = "__all__"
        fields = ('user_title',)
