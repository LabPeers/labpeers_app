#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:00:53 2019

@author: egetenmeyer
"""
from django.contrib.postgres.fields import ArrayField
from django import forms
from .models import Post
from django.db import models


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter the plot title here...'
        }
    ))
    
    myX = ArrayField(models.IntegerField())
    

    class Meta:
        model = Post
        fields = ('post','myX',)
#        fields = "__all__"
