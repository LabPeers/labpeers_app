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
from django.contrib import messages
from django.forms import modelformset_factory


from bokeh.plotting import figure , curdoc , show , output_file
from bokeh.resources import CDN
from bokeh.embed import components
import pandas as pd
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter, HoverTool
from bokeh.palettes import Viridis256
from bokeh.transform import transform
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

#from bokeh.models import ColumnDataSource, ColorBar
#from bokeh.palettes import Spectral6
#from bokeh.transform import linear_cmap


########
 
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
from bokeh.io import export_png
from bokeh.io.export import get_screenshot_as_png
########

#from django.template.defaultfilters import slugify

#from .models import Greeting 
from .models import Graph_Data, Gallery_Plots
from .forms import HomeForm, GalleryForm

from accounts.forms import UserProfileForm
from accounts.models import UserProfile



from django.core.files.uploadedfile import InMemoryUploadedFile




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
    
    return plotdict, plot







class HomeReal(TemplateView):
    template_name = './home.html'
  
    

class Profile(TemplateView):
    template_name = './profile.html' 
    
    def get(self, request):
        
        p_form = UserProfileForm(instance=request.user.userprofile)
        args = {'user': request.user, 'p_form': p_form}
        
        return render(request, self.template_name, args)
    
    def post(self,request):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:
            #raise Http404
        
            #p_form = UserProfileForm(request.POST or None, request.FILES or None) # A form bound to the POST data
            p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile) # A form bound to the POST data
            
            if p_form.is_valid():
                #p_form = p_form.save(commit=False)
                #p_form.user = request.user
                p_form.save()
              #  return HttpResponseRedirect(instance.get_absolute_url())
                messages.success(request, f'Image successfully uploaded!')
                return redirect('profile')
            
            args = {'user': request.user,'p_form':p_form}
                
            return render(request, self.template_name, args)  



#def youfunc(request):
#    youtemplate = UserProfileForm()
#    if request.method == 'POST':
#        youform = UserProfileForm(request.POST, request.FILES)
#        if youform.is_valid():
#           youform.save()
#           #return HttpResponseRedirect('http://www.You.url') # or other
#    #youquery = .objects.order_by('image').last()
#    return render(request, "YouProject/YouHtml.html", {'youtemplate': youtemplate})

   
    

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
        formplot = GalleryForm()
        
        #users = User.objects.exclude(id=request.user.id)
        #plot = figure(plot_width=600, plot_height=600, title='Your title will go here')
        #script, div = components(plot, CDN)
        
        ########### -----DATA TABLE----- ########### 
        
        plotdict=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
#        x = plotdict["the_script"]
#        y = plotdict["the_div"]
     #  script, div = components({'plot': plot})
        dict2={"form":form,"formplot":formplot}
        dict3={**plotdict , **dict2}
        
     
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:
            #raise Http404
        
            form = HomeForm(request.POST) # A form bound to the POST data
            formplot = GalleryForm()
    
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
                    instance.user=request.user
                    instance.save()
                                
#                    myfilename=form.cleaned_data['graph_filename']
#                    myslug=slugify(myfilename)
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
                plotdict, plot =bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
                
                
                if 'make_png' in request.POST:
                    print("1 I'm in the make png loop now!")
                    formplot = GalleryForm(request.POST)
            
                    if formplot.is_valid():
                        print("2 I'm in the make png loop now!")
                        instance2=formplot.save(commit=False)
                        myplotname=formplot.cleaned_data['plotname']
                        instance2.plotname=myplotname
                        instance2.user=request.user


                        
                        #Testplot
                        
#                        filename="/plots/" + myplotname + ".png"
#                        print(filename)
#                        newplot=export_png(plot)
#                        print(newplot)
                        
                        
                        #figure = io.BytesIO()
#                        plot = figure(plot_width=600, plot_height=600, title=mytitle, 
#                                          x_axis_label=myXlabel, y_axis_label=myYlabel)
                        
                        pillow_image = get_screenshot_as_png(plot)
                        
                        
                        image_field = instance2.myplots
                        img_name = myplotname + '.png'
 #                       img_path = settings.MEDIA_ROOT + img_name
#                        img_path = "/plots/" + img_name
                        
                        f = BytesIO()
                        
                        try: 
                            pillow_image.save(f, format = 'png')
                            image_field.save(img_name, ContentFile(f.getvalue()))
                        
                        finally:
                            f.close()
                        
                      
                        
                        #newplot=export_png(plot)
                        
                        instance2.save()                    
                    
                        formplot = GalleryForm(request.POST)
                

                
                dict2={"form":form,"formplot":formplot}
                dict3={**plotdict , **dict2}
                    
                    
                    
                form = HomeForm(request.POST)
                formplot = GalleryForm(request.POST or None)
                    

            
                return render(request, self.template_name, dict3)
                
            
            else:
                return redirect("bubblechart")
            
            
            
    
        else:
            return redirect("login")


    

    
class EditView(TemplateView):
    template_name = './bubblechart.html'     
    
    
    def get(self,request,pk):
        if request.user.is_authenticated:
#        #        graph_data=Graph_Data.objects.get(pk=self.kwargs.get('pk'))
            
            formplot = GalleryForm()

            graph_data=Graph_Data.objects.get(pk=pk)    
        
        
           # form=graph_data
#            form = HomeForm()
#            graph_data=Graph_Data.objects.get(pk=pk)
#            form=graph_data
            instance = get_object_or_404(Graph_Data, pk=pk)
            form = HomeForm(request.POST or None, instance=instance)
            
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
            plotdict, plot =bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
            dict2={"form":form,"formplot":formplot}
            dict3={**plotdict , **dict2}
                

 
        #form = HomeForm(request.POST)

            
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request,pk):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:

            #raise Http404
            
            instance = get_object_or_404(Graph_Data, pk=pk)
            form = HomeForm(request.POST or None, instance=instance)
            formplot = GalleryForm()
#                if form.is_valid():
#                    instance = form.save(commit=False)
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
                    
#                    myfilename=form.cleaned_data['graph_filename']
#                    myslug=slugify(myfilename)
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
                plotdict, plot=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist)
                
                if 'make_png' in request.POST:
                    print("1Edit I'm in the make png loop now!")
                    formplot = GalleryForm(request.POST)
            
                    if formplot.is_valid():
                        print("2Edit I'm in the make png loop now!")
                        myplotname=formplot.cleaned_data['plotname']
                        newplot=export_png(plotdict, filename=myplotname + ".png")
                        plotimage= Gallery_Plots(plotname=myplotname, myplots=newplot)
                        plotimage.save()    
                        formplot = GalleryForm(request.POST)
                

                
                dict2={"form":form,"formplot":formplot}
                dict3={**plotdict , **dict2}
                

 
                form = HomeForm(request.POST)
                formplot = GalleryForm()
                    
                    
                return render(request, self.template_name, dict3)
            
            else: 
                    
                return redirect("bubblechart")
            
    
        else:
            return redirect("login")





class GalleryView(TemplateView):
    template_name = './gallery.html'  
      
    def get(self, request):
        gallery_plots=Gallery_Plots.objects.filter(user=request.user)
       # myfilename=graph_data.graph_filename
       # mydate=graph_data.myDate
        return render(request, self.template_name, 
                      {'gallery_plots' : gallery_plots})
