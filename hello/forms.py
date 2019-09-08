#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:00:53 2019

@author: egetenmeyer
"""
from django.contrib.postgres.fields import ArrayField
from django import forms
from .models import Graph_title
from django.db import models


class HomeForm(forms.ModelForm):
    graph_title = forms.CharField(widget=forms.Textarea)
    
    #myX = ArrayField(models.IntegerField())
    

    class Meta:
        model = Graph_title
        #fields = ('post','myX',)
        fields = "__all__"
#        fields = ('graph_title',)
