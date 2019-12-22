# =============================================================================
# from django.shortcuts import render
# from django.http import HttpResponse
# 
# #from django.shortcuts import render_to_response
# from django.template import RequestContext
# from .models import InputForm
# from .compute import compute
# 
# import requests
# 
# from .models import Greeting
# =============================================================================

# Create your views here.
#def index(request):
    # return HttpResponse('Hello from Python!')
 #   return render(request, "index.html")
from django.views.generic import TemplateView
from django.views.generic.edit import FormView 
from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from bokeh.plotting import figure , curdoc , show , output_file
from bokeh.resources import CDN
from bokeh.embed import components
import pandas as pd
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter, HoverTool
from bokeh.palettes import Viridis256
from bokeh.transform import transform
import numpy as np


#from bokeh.models import ColumnDataSource, ColorBar
#from bokeh.palettes import Spectral6
#from bokeh.transform import linear_cmap


#from .models import Greeting 
from .models import Graph_Data
from .forms import HomeForm
from django.contrib.auth.models import User


########
from datetime import date
from random import randint
 
from bokeh.client import push_session
from bokeh.document import Document
from bokeh.models.glyphs import Line, Circle
from bokeh.models import (
    Plot, ColumnDataSource, DataRange1d,
    LinearAxis, DatetimeAxis, Grid, HoverTool
)
from bokeh.models.widgets import (
    Button, TableColumn, DataTable,
    DateEditor, DateFormatter, IntEditor)
from bokeh.models.layouts import WidgetBox, Column
########

#from django.template.defaultfilters import slugify

from django.shortcuts import get_object_or_404





def bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist):
    d = {'myXaxis': myXlist, 'myYaxis': myYlist, 'myBubble': myRlist} 

    df = pd.DataFrame(data = d)
    source = ColumnDataSource(df)
    plot = figure(plot_width=600, plot_height=600, title=mytitle, 
                  x_axis_label=myXlabel, y_axis_label=myYlabel)

    color_mapper = LinearColorMapper(palette = Viridis256, low = min(df['myBubble']), 
                                             high = max(df['myBubble']))
            #color_mapper = LinearColorMapper(palette = Viridis256, low = min(myRlist), high = max(myRlist))
    color_bar = ColorBar(color_mapper = color_mapper,
                         location = (0, 0),
                         ticker = BasicTicker())
    plot.add_layout(color_bar, 'right')
    plot.scatter(x = 'myXaxis', y = 'myYaxis', size = 'myBubble', legend = None, 
                 fill_color = transform('myBubble', color_mapper), source = source)
    plot.add_tools(HoverTool(tooltips = [('Count', '@myBubble')]))
    
    script, div = components({'plot': plot})
    plotdict={"the_script": script, "the_div": div}
    
    return plotdict







class HomeReal(TemplateView):
    template_name = './home.html'
    

class Profile(TemplateView):
    template_name = './profile.html'  
    

class Projects(TemplateView):
    template_name = './projects.html'
    
    def get(self, request):
        graph_data=Graph_Data.objects.filter(user=request.user)
       # myfilename=graph_data.graph_filename
       # mydate=graph_data.myDate
        return render(request, self.template_name, 
                      {'graph_data' : graph_data})
        

class DeleteView(TemplateView):
    template_name = './projects.html'
  
#if request.method == 'POST': # If the form has been submitted...
    def get(self,request,pk):
    
        if request.user.is_authenticated:
            #raise Http404
            data_row_old=Graph_Data.objects.get(pk=pk)
            data_row_old.delete()
            
            return redirect('projects')
        

   
    
class HomeView(TemplateView):
    template_name = './bubblechart.html' 
    
    
    def get(self,request):
        
        myXlist=[1,2]
        myYlist=[3,4]
        myRlist=[10,50]
        mytitle='Your title will go here'
        myXlabel='x-axis label'
        myYlabel='y-axis label'
        
        
        
        form = HomeForm()
        #users = User.objects.exclude(id=request.user.id)
        #plot = figure(plot_width=600, plot_height=600, title='Your title will go here')
        #script, div = components(plot, CDN)
        
        ########### -----DATA TABLE----- ########### 
        
        plotdict=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
#        x = plotdict["the_script"]
#        y = plotdict["the_div"]
     #  script, div = components({'plot': plot})
        dict2={"form":form}
        dict3={**plotdict , **dict2}
        
     
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:
            #raise Http404
        
            form = HomeForm(request.POST) # A form bound to the POST data
    
    
            if form.is_valid():
            
            #form.save()
                #Avoid rows with same filename!!
                myfilename=form.cleaned_data['graph_filename']
                graph_data=Graph_Data.objects.filter(user=request.user)
                filename_list=graph_data.values_list('graph_filename',flat=True)
                filename_list2=list(filename_list)
                print('HELLO')
                print(filename_list)
                print(filename_list2)
                print(myfilename)
                if myfilename in filename_list:
                    repeat=Graph_Data.objects.get(graph_filename=myfilename)
                    x=repeat.id
                    print(x)
                    
                    instance=get_object_or_404(Graph_Data,id = x)
                    form = HomeForm(request.POST or None, instance=instance)
                    if form.is_valid():
                        instance = form.save(commit=False)

                else:
                  instance=form.save(commit=False)  

                
              #  instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                
#                myfilename=form.cleaned_data['graph_filename']
#                myslug=slugify(myfilename)
                mytitle=form.cleaned_data['graph_title']
                myXlabel=form.cleaned_data['graph_xlabel']
                myYlabel=form.cleaned_data['graph_ylabel']
            
                myXdata=form.cleaned_data['myX']
                myXlist=myXdata.split(",")
                myYdata=form.cleaned_data['myY']
                myYlist=myYdata.split(",")
                myRdata=form.cleaned_data['myRadius']
                myRlist=myRdata.split(",")
                myRlist=np.array(myRlist, dtype=np.float32)
#            
            
            #scale = 10
                plotdict=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
                dict2={"form":form}
                dict3={**plotdict , **dict2}
                

 
                form = HomeForm(request.POST)
            

            
                return render(request, self.template_name, dict3)
            
            else:
                return redirect("bubblechart")
                
    
        else:
            return redirect("login")

    

    
class EditView(TemplateView):
    template_name = './bubblechart.html'     
    
    
    def get(self,request,pk):
        if request.user.is_authenticated:
        
#        graph_data=Graph_Data.objects.get(pk=self.kwargs.get('pk'))

            graph_data=Graph_Data.objects.get(pk=pk)    
        
        
            form=graph_data
                
            mytitle=graph_data.graph_title
            myXlabel=graph_data.graph_xlabel
            myYlabel=graph_data.graph_ylabel
            
            myXdata=graph_data.myX
            myXlist=myXdata.split(",")
            myYdata=graph_data.myY
            myYlist=myYdata.split(",")
            myRdata=graph_data.myRadius
            myRlist=myRdata.split(",")
            myRlist=np.array(myRlist, dtype=np.float32)
#            
            
            #scale = 10
            plotdict=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
            dict2={"form":form}
            dict3={**plotdict , **dict2}
                

 
        #form = HomeForm(request.POST)

            
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request,pk):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:
            #raise Http404
            
            instance = get_object_or_404(Graph_Data, pk=pk)
            form = HomeForm(request.POST or None, instance=instance)
#            if form.is_valid():
#                instance = form.save(commit=False)
            if form.is_valid():

                myfilename=form.cleaned_data['graph_filename']
                graph_data=Graph_Data.objects.filter(user=request.user)
                filename_list=graph_data.values_list('graph_filename',flat=True)
                filename_list2=list(filename_list)
                print('HELLO')
                print(filename_list)
                print(filename_list2)
                print(myfilename)
                    
                if myfilename in filename_list:
                    repeat=Graph_Data.objects.get(graph_filename=myfilename)
                    x=repeat.id
                    print(x)
                    
                    instance=get_object_or_404(Graph_Data,id = x)
                    form = HomeForm(request.POST or None, instance=instance)
                    if form.is_valid():
                        instance = form.save(commit=False)
                    else:
                        return redirect("bubblechart")

                else:
                  instance=form.save(commit=False)  

            
            #form.save()
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                
#                myfilename=form.cleaned_data['graph_filename']
#                myslug=slugify(myfilename)
                mytitle=form.cleaned_data['graph_title']
                myXlabel=form.cleaned_data['graph_xlabel']
                myYlabel=form.cleaned_data['graph_ylabel']
            
                myXdata=form.cleaned_data['myX']
                myXlist=myXdata.split(",")
                myYdata=form.cleaned_data['myY']
                myYlist=myYdata.split(",")
                myRdata=form.cleaned_data['myRadius']
                myRlist=myRdata.split(",")
                myRlist=np.array(myRlist, dtype=np.float32)
#            
            
                #scale = 10
                plotdict=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
                dict2={"form":form}
                dict3={**plotdict , **dict2}
                

 
                form = HomeForm(request.POST)

            
                return render(request, self.template_name, dict3)
            
            else: 

                return redirect("bubblechart")
    
        else:
            return redirect("login")
