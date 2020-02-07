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

from bokeh.io.export import get_screenshot_as_png



########

#from django.template.defaultfilters import slugify

#from .models import Greeting 
from .models import Tracking_Data
from .forms import TrackingForm
from bubble.forms import GalleryForm
from bubble.models import Gallery_Plots










def trackingplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist, mySymbol):
#    myscale=1
#    myRlist=[x / abs(myscale) for x in myRlist]
#    
    
    
    
    d = {'myXaxis': myXlist, 'myYaxis': myYlist, 'myError': myRlist, 'mySymbol': mySymbol}



    df = pd.DataFrame(data = d)
    source = ColumnDataSource(df)
#    plot = figure(plot_width=600, plot_height=600, title=mytitle, 
#                  x_axis_label=myXlabel, y_axis_label=myYlabel)
    
    #Scaled myRlist
    BiggestBubble=max(myRlist)
    FirstScale=BiggestBubble/10
    x1=min(myXlist)
    index_x1=myXlist.argmin()
    print(index_x1)
    myr1=myRlist[index_x1]
    print(myr1)
    #myxmin=x1 - 0.7 * myr1/FirstScale
    myxmin=x1 - FirstScale
    print(myxmin)
    
    x2=max(myXlist)
    index_x2=myXlist.argmax()
    myr2=myRlist[index_x2]
    #myxmax=x2 + 0.7 * myr2/FirstScale
    myxmax=x2 + FirstScale
    
    y1=min(myYlist)
    index_y1=myYlist.argmin()
    myr3=myRlist[index_y1]
    #myymin=y1 - 0.7 * myr3/FirstScale
    myymin=y1 - FirstScale
    
    y2=max(myYlist)
    index_y2=myYlist.argmax()
    myr4=myRlist[index_y2]
    #myymax=y2 + 0.7 * myr4/FirstScale
    myymax=y2 + FirstScale
    
    
#    start=min(myRlist)
#    end=max(myRlist)
#    slider = Slider(start, end, value=1, step=abs(end-start)/100, title="Bubble size scaling factor")
# 
    
    
    plot = figure(title=mytitle, x_axis_label=myXlabel, y_axis_label=myYlabel, 
                  x_range=(myxmin, myxmax), y_range=(myymin, myymax))

    #For mobile and desktop automatic resizing
    plot.sizing_mode = "scale_width"



    #plot.circle(x = 'myXaxis', y = 'myYaxis', size=15,
     #            line_color="navy", fill_color="orange", alpha=0.5)
    
    plot.circle(x = 'myXaxis', y = 'myYaxis', size=15, color ="orange", source=source)
    
    
    
    #plot.add_tools(HoverTool(tooltips = [('Count', '@myError')]))
   # plot.add_tools(slider)


    script, div = components({'plot': plot})
    plotdict={"the_script": script, "the_div": div}
    
    return plotdict, plot



   
    
class TrackView(TemplateView):
    template_name = './track.html' 
    
    
    def get(self,request):
        
        myXlist='1,3'
        myYlist='3,4'
        myRlist='10,50'
        myScale=1
        mytitle='Your title will go here'
        myXlabel='x-axis label'
        myYlabel='y-axis label'
        
        myXlist=myXlist.split(",")
        myXlist=np.array(myXlist, dtype=np.float32)
        myYlist=myYlist.split(",")
        myYlist=np.array(myYlist, dtype=np.float32)
        myRlist=myRlist.split(",")
        myRlist=np.array(myRlist, dtype=np.float32)
        
        
        
        form = TrackingForm()
        formplot = GalleryForm()
        mySymbol='x';
        
     
        plotdict , plot =trackingplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,mySymbol)
        
#        x = plotdict["the_script"]
#        y = plotdict["the_div"]
     #  script, div = components({'plot': plot})
        dict2={"form":form,"formplot":formplot}
        dict3={**plotdict , **dict2}
#        dict4={**dict3, **tabledict}
     
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:
            #raise Http404
        
            form = TrackingForm(request.POST) # A form bound to the POST data
            formplot = GalleryForm()
    
            if form.is_valid():
            
                    #form.save()
                    #Avoid rows with same filename!!
                myfilename=form.cleaned_data['graph_filename']
                tracking_data=Tracking_Data.objects.filter(user=request.user)
                filename_list=tracking_data.values_list('graph_filename',flat=True)
                filename_list2=list(filename_list)
                print('HELLO WORLD!!')
                print(filename_list)
                print(filename_list2)
                print(myfilename)
                if myfilename in filename_list:
                    repeat=Tracking_Data.objects.get(graph_filename=myfilename)
                    x=repeat.id
                    print(x)
                    
                    instance=get_object_or_404(Tracking_Data,id = x)
                    form = TrackingForm(request.POST or None, instance=instance)
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
                myXlist=np.array(myXlist, dtype=np.float32)
                myYdata=form.cleaned_data['myY']
                myYlist=myYdata.split(",")
                myYlist=np.array(myYlist, dtype=np.float32)
                myRdata=form.cleaned_data['myError']
                myRlist=myRdata.split(",")
                myRlist=np.array(myRlist, dtype=np.float32)
                mySymbol=form.cleaned_data['mySymbol']
#                
                    
                    #scale = 10
                plotdict, plot =trackingplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,mySymbol)
                
                
                if 'make_png' in request.POST:
                    print("1 I'm in the make png loop now!")
                    formplot = GalleryForm(request.POST)
            
                    if formplot.is_valid():
                        print("2 I'm in the make png loop now!")
                        instance2=formplot.save(commit=False)
                        myplotname=formplot.cleaned_data['plotname']
                        instance2.plotname=myplotname
                        instance2.user=request.user
                        
                        pillow_image = get_screenshot_as_png(plot)
                        
                        
                        image_field = instance2.myplots
                        img_name = myplotname + '.png'
                        
                        f = BytesIO()
                        
                        try: 
                            pillow_image.save(f, format = 'png')
                            image_field.save(img_name, ContentFile(f.getvalue()))
                        
                        finally:
                            f.close()
                        
                        #newplot=export_png(plot)
                        
                        instance2.save()                    
                    
                        formplot = GalleryForm(request.POST)
                

                mypkX=myXdata
                mypkY=myYdata
                mypkError=myRdata
                
                dict2={"form":form,"formplot":formplot,"mypkX":mypkX,"mypkY":mypkY,"mypkError":mypkError}
                dict3={**plotdict , **dict2}
                    
                    
                    
                form = TrackingForm(request.POST)
                formplot = GalleryForm(request.POST or None)
                
                
                        ########### -----DATA TABLE----- ########### 
#                dict_table = {
#                        'myXlist': myXlist,
#                        'myYlist': myYlist,
#                        'myRlist': myRlist,
#                        }
#                source = ColumnDataSource(data=dict_table)
#
#                #old_source = ColumnDataSource(copy.deepcopy(dict_table))
#
#                columns = [
#                        TableColumn(field="myXlist", title="X-values"),
#                        TableColumn(field="myYlist", title="Y-values"),
#                        TableColumn(field="myRlist", title="Bubble size"),
#                ]
#
#                data_table = DataTable(
#                        source=source,
#                        columns=columns,
#                        width=800,
##                        editable=True,
##                        reorderable=False,
#                        )

#                def on_change_data_source(attr, old, new):
#                    # old, new and source.data are the same dictionaries
#                    print('-- SOURCE DATA: {}'.format(source.data))
#                    print('>> OLD SOURCE: {}'.format(old_source.data))
#                    
#                    # to check changes in the 'y' column:
#                    indices = list(range(len(old['y'])))
#                    changes = [(i,j,k) for i,j,k in zip(indices, old_source.data['y'], source.data['y']) if j != k]
#                    print('>> CHANGES: {}'.format(changes))
#                    
#                    old_source.data = copy.deepcopy(source.data)
#
#        
#    
#                print('SOURCE DATA: {}'.format(source.data))
#
#
#                data_table.source.on_change('data', on_change_data_source)
#
#                curdoc().add_root(data_table)
#        
#                script_t, div_t = components({'data_table': data_table})
#                tabledict={"the_script_t": script_t, "the_div_t": div_t}
    
                ########### -----DATA TABLE END----- ###########
                
                
                
                #dict4={**dict3, **tabledict}
                
                
                
                

            
                return render(request, self.template_name, dict3)
                
            
            else:
                return redirect("track")
            
            
            
    
        else:
            return redirect("login")


    

    
class EditTrackView(TemplateView):
    template_name = './tack.html'     
    
    
    def get(self,request,pk):
        if request.user.is_authenticated:

            
            formplot = GalleryForm()

            tracking_data=Tracking_Data.objects.get(pk=pk)
            mypkX=tracking_data.myX
            mypkY=tracking_data.myY
            mypkError=tracking_data.myError
        

            instance = get_object_or_404(Tracking_Data, pk=pk)
            form = TrackingForm(request.POST or None, instance=instance)
            
            mytitle=tracking_data.graph_title
            myXlabel=tracking_data.graph_xlabel
            myYlabel=tracking_data.graph_ylabel
            myXdata=tracking_data.myX
            myXlist=myXdata.split(",")
            myXlist=np.array(myXlist, dtype=np.float32)
            myYdata=tracking_data.myY
            myYlist=myYdata.split(",")
            myYlist=np.array(myYlist, dtype=np.float32)
            myRdata=tracking_data.myError
            myRlist=myRdata.split(",")
            myRlist=np.array(myRlist, dtype=np.float32)
            mySymbol=tracking_data.mySymbol
            
#            
            
            #scale = 10
            plotdict, plot =trackingplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,mySymbol)
            dict2={"form":form,"formplot":formplot,"mypkX":mypkX,"mypkY":mypkY,"mypkError":mypkError}
            dict3={**plotdict , **dict2}
                

 
        #form = HomeForm(request.POST)

            
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request,pk):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:

            #raise Http404
            
            instance = get_object_or_404(Tracking_Data, pk=pk)
            form = TrackingForm(request.POST or None, instance=instance)
            formplot = GalleryForm()
#                if form.is_valid():
#                    instance = form.save(commit=False)
            if form.is_valid():
                    
                myfilename=form.cleaned_data['graph_filename']
                tracking_data=Tracking_Data.objects.filter(user=request.user)
                filename_list=tracking_data.values_list('graph_filename',flat=True)
                filename_list2=list(filename_list)
                print('HELLO')
                print(filename_list)
                print(filename_list2)
                print(myfilename)
                        
                if myfilename in filename_list:
                    repeat=Tracking_Data.objects.get(graph_filename=myfilename)
                    x=repeat.id
                    print(x)
                
                    instance=get_object_or_404(Tracking_Data,id = x)
                    form = TrackingForm(request.POST or None, instance=instance)
                    if form.is_valid():
                        instance = form.save(commit=False)
                    else:
                        return redirect("track")
                            
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
                myXlist=np.array(myXlist, dtype=np.float32)
                myYdata=form.cleaned_data['myY']
                myYlist=myYdata.split(",")
                myYlist=np.array(myYlist, dtype=np.float32)
                myRdata=form.cleaned_data['myError']
                myRlist=myRdata.split(",")
                myRlist=np.array(myRlist, dtype=np.float32)
                mySymbol=form.cleaned_data['mySymbol']
                    
                    #scale = 10
                plotdict, plot=trackingplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,mySymbol)
                
                if 'make_png' in request.POST:
                    print("1 I'm in the make png loop now!")
                    formplot = GalleryForm(request.POST)
            
                    if formplot.is_valid():
                        print("2 I'm in the make png loop now!")
                        instance2=formplot.save(commit=False)
                        myplotname=formplot.cleaned_data['plotname']
                        instance2.plotname=myplotname
                        instance2.user=request.user
                        
                        pillow_image = get_screenshot_as_png(plot)
                        
                        
                        image_field = instance2.myplots
                        img_name = myplotname + '.png'
                        
                        f = BytesIO()
                        
                        try: 
                            pillow_image.save(f, format = 'png')
                            image_field.save(img_name, ContentFile(f.getvalue()))
                        
                        finally:
                            f.close()
                        
                        #newplot=export_png(plot)
                        
                        instance2.save()                    
                    
                        formplot = GalleryForm(request.POST)
   


             
                mypkX=myXdata
                mypkY=myYdata
                mypkError=myRdata
                
                dict2={"form":form,"formplot":formplot,"mypkX":mypkX,"mypkY":mypkY,"mypkError":mypkError}
                dict3={**plotdict , **dict2}
                

 
                form = TrackingForm(request.POST)
                formplot = GalleryForm()
                    
                    
                return render(request, self.template_name, dict3)
            
            else: 
                    
                return redirect("track")
            
    
        else:
            return redirect("login")





class GalleryView(TemplateView):
    template_name = './gallery.html'  
      
    def get(self, request):
        gallery_plots=Gallery_Plots.objects.filter(user=request.user)

        return render(request, self.template_name, 
                      {'gallery_plots' : gallery_plots})
