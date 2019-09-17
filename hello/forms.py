#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:00:53 2019

@author: egetenmeyer
"""
from django.contrib.postgres.fields import ArrayField
from django import forms
from .models import Graph_Data
from django.db import models


class HomeForm(forms.ModelForm):
    graph_title = forms.CharField(widget=forms.TextInput())
    myX = forms.CharField(widget=forms.TextInput())
    myY = forms.CharField(widget=forms.TextInput())
#    myRadius= forms.CharField(widget=forms.TextInput())
    

    class Meta:
        model = Graph_Data
        #fields = ('post','myX',)
#        fields = "__all__"
        fields = ('graph_title','myX','myY','myRadius',)
