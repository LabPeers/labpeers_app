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
#from .models import Graph_Data
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



class HomeReal(TemplateView):
    template_name = './home.html'
    

class Profile(TemplateView):
    template_name = './profile.html'    



# =============================================================================
# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             login(request, user)
#             return redirect("home")
# 
#         else:
#             for msg in form.error_messages:
#                 print(form.error_messages[msg])
# 
#             return render(request = request,
#                           template_name = "./register.html",
#                           context={"form":form})
# 
#     form = UserCreationForm
#     return render(request = request,
#                   template_name = "./register.html",
#                   context={"form":form})
# =============================================================================
# =============================================================================
# 
# class Register(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'register.html'
# 
# =============================================================================

# =============================================================================
# class Register(FormView):
#      template_name = './register.html'
#      userform = UserCreationForm
#  
#      
#      def get(self,request):        
#          userform = UserCreationForm        
#          return render(request, self.template_name, {"userform": userform})
#   
#      def post(self,request):
#          userform = UserCreationForm(request.POST) # A form bound to the POST data
#          if userform.is_valid():
#              user=userform.save()
#              username = userform.cleaned_data.get('username')
#              login(request, user)
#              return redirect("home")
#  
#          else:
#              for msg in userform.error_messages:
#                  print(userform.error_messages[msg])
#                  
#              return render(request, self.template_name, {"userform":userform})
#  
#           #userform = UserCreationForm
#           #return render(request, self.template_name,{"userform":userform} )
#      
# =============================================================================
     
    
class HomeView(TemplateView):
    template_name = './bubblechart.html' 
    
    
    def get(self,request):
        
        form = HomeForm()
        #users = User.objects.exclude(id=request.user.id)
        plot = figure(plot_width=600, plot_height=600, title='Your title will go here')
        #script, div = components(plot, CDN)
        
        ########### -----DATA TABLE----- ########### 
        myXlist=[]
        myYlist=[]
        myRlist=[]
        d1 = {'myXaxis': myXlist, 'myYaxis': myYlist, 'myBubble': myRlist} 
        df1 = pd.DataFrame(data = d1)
        source1=ColumnDataSource(df1)
        columns = [
        TableColumn(field="myXlist", title="X-values", editor=DateEditor()),
        TableColumn(field="myYlist", title="Y-values", editor=IntEditor()),
        ]
        table = DataTable(source=source1, columns=columns, width=400, height=400, editable=True)
        script, div = components({'plot': plot,'table': table})
     
        return render(request, self.template_name, {"the_script": script, "the_div": div, 
                                                    "form": form})
        #return render(request, self.template_name, {"users": users, "the_script": script, "the_div": div, 
         #                                           "form": form})
    
    
    def post(self,request):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:
            #raise Http404
        
            form = HomeForm(request.POST) # A form bound to the POST data
    
    
            if form.is_valid():
            
            #form.save()
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
              #  graph_filename=form.cleaned_data['graph_filename']
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
                d = {'myXaxis': myXlist, 'myYaxis': myYlist, 'myBubble': myRlist} 

                df = pd.DataFrame(data = d)
                source = ColumnDataSource(df)
                plot = figure(plot_width=600, plot_height=600, title=mytitle, x_axis_label=myXlabel, y_axis_label=myYlabel)

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



            
            #script, div = components(plot, CDN)      
            
            
#            graph_title.user = request.user
#            graph_title.save()

#            mytitle = form.cleaned_data['graph_title']

            #postall.save()
            
           #script, div = mainplot(form)            #form.save(commit=False)

            #mytitle = form.post
            
            #mytitle = Graph_title.objects.all()
 
                form = HomeForm()
            
            #form=HomeForm()

########### -----DATA TABLE----- ########### 
           
                columns = [
                        TableColumn(field="myXlist", title="X-values", editor=DateEditor()),
                        TableColumn(field="myYlist", title="Y-values", editor=IntEditor()),
                        ]
                table = DataTable(source=source, columns=columns, width=400, height=400, editable=True)

                script, div = components({'plot': plot,'table': table})
            
            return render(request, self.template_name, {"the_script": script, "the_div": div, "form": form})
    
        else:
            return redirect("login")


