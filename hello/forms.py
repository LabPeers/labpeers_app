#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:00:53 2019

@author: egetenmeyer
"""
from django import forms
from .models import Graph_Data



class HomeForm(forms.ModelForm):
    graph_filename=forms.CharField(widget=forms.TextInput())
    graph_title = forms.CharField(required=False, widget=forms.TextInput())
    graph_xlabel = forms.CharField(required=False, widget=forms.TextInput())
    graph_ylabel = forms.CharField(required=False, widget=forms.TextInput())
    myX = forms.CharField(widget=forms.TextInput())
    myY = forms.CharField(widget=forms.TextInput())
    myRadius= forms.CharField(widget=forms.TextInput())
    

    class Meta:
        model = Graph_Data
        #fields = ('post','myX',)
#        fields = "__all__"
        fields = ('graph_filename','graph_title','graph_xlabel','graph_ylabel',
                  'myX','myY','myRadius',)
