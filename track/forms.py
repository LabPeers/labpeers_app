#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:00:53 2019

@author: egetenmeyer
"""
from django import forms
from .models import Graph_Data, Gallery_Plots

MARKER_CHOICES=[
    ('o+', 'Circle and Cross'),
    ('square_cross', 'Square and Cross'),
    ('diamond', 'Diamond'),
    ('+', 'cross'),
    ('ox', 'Circle and x'),
    ('square_x', 'Square and x'),
    ('inverted_triangle', 'Up-side-down triangle'),
    ('x', 'x'),
    ('o', 'Circle'),
    ('square', 'Square'),
    ('triangle', 'Triangle'),
    ('*', 'Asterisk *'),
    ]

class HomeForm(forms.ModelForm):
    graph_filename=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'e.g. MyFilename'}))
    graph_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. MyTitle'}))
    graph_xlabel = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. x-axis'}))
    graph_ylabel = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. y-axis'}))
    graph_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'e.g. This graph is very important!',
                                                                                     'style': 'height: 60px;'}))
    myX = forms.CharField(widget=forms.TextInput(attrs={'id':'x-values','placeholder':'e.g. 1,2,3'}))
    myY = forms.CharField(widget=forms.TextInput(attrs={'id':'y-values','placeholder':'e.g. 1,5,9'}))
    myError= forms.CharField(widget=forms.TextInput(attrs={'id':'Bubble-size','placeholder':'e.g. 5,10,30'}))
    mySymbol=forms.CharField(label='Choose your marker symbol!', widget=forms.Select(choices=MARKER_CHOICES))
   # slug=forms.SlugField(widget=forms.TextInput())
    

    class Meta:
        model = Graph_Data
        #fields = ('post','myX',)
#        fields = "__all__"
        fields = ('graph_filename','graph_title','graph_xlabel','graph_ylabel','graph_description',
                  'myX','myY','myRadius','myScale',)



class GalleryForm(forms.ModelForm):
    plotname=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'e.g. MyPlot'}))
    
    class Meta:
        model = Gallery_Plots
        fields = ('plotname',)
