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

from .models import Graph_Data, Gallery_Plots
from .forms import HomeForm, GalleryForm
from myscatter.models import Tracking_Data
from accounts.models import UserProfile

from accounts.forms import UserProfileForm


from django import http
from django.views.generic import RedirectView

import boto3

#from boto3.s3.connection import S3Connection

from gettingstarted.settings import AWS_ACCESS_KEY_ID
from gettingstarted.settings import AWS_SECRET_ACCESS_KEY
from gettingstarted.settings import AWS_STORAGE_BUCKET_NAME
from gettingstarted.settings import MEDIA_URL

import logging
from botocore.client import Config





def bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist, myScale):
#    myscale=1
#    myRlist=[x / abs(myscale) for x in myRlist]
#    
    
    myRlist2=myRlist/myScale
    
    d = {'myXaxis': myXlist, 'myYaxis': myYlist, 'myBubble': myRlist, 'myBubble2': myRlist2, 'myScale' : myScale}



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

    plot.sizing_mode = "scale_width"


    LabPeers = ['#000000','#12030E','#25071C','#380A2B','#4A0E39','#5D1248',
                    '#701556','#821964','#951C73','#A82081','#BB2490','#BB2490',
                    '#C1399B','#C84FA6','#CF65B1','#D67BBC','#DD91C7','#E3A7D2',
                    '#EABDDD','#F1D3E8','#F8E9F3','#FFFFFF']




    color_mapper = LinearColorMapper(palette = LabPeers, low = min(df['myBubble']), 
                                             high = max(df['myBubble']))
            #color_mapper = LinearColorMapper(palette = Viridis256, low = min(myRlist), high = max(myRlist))
    color_bar = ColorBar(color_mapper = color_mapper,
                         location = (0, 0),
                         ticker = BasicTicker())
    plot.add_layout(color_bar, 'right')
    plot.scatter(x = 'myXaxis', y = 'myYaxis', size = 'myBubble2', legend = None, 
                 fill_color = transform('myBubble', color_mapper), source = source)
    plot.add_tools(HoverTool(tooltips = [('Count', '@myBubble')]))
   # plot.add_tools(slider)


    script, div = components({'plot': plot})
    plotdict={"the_script": script, "the_div": div}
    
    return plotdict, plot







class HomeReal(TemplateView):
    template_name = './home.html'
    
    
    

#Make image secret

logger = logging.getLogger('django.request')  
    
class SecretFileView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
#        s3 = S3Connection(AWS_ACCESS_KEY_ID,
#                            AWS_SECRET_ACCESS_KEY,
#                            is_secure=True)
        

        session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                )
        
        s3 = session.resource('s3')
        
        s3Client = boto3.client('s3', region_name='us-east-2')# config=Config(signature_version='s3v4'))
        #s3Client.generate_presigned_url('get_object', Params = {'Bucket': 'www.mybucket.com', 'Key': 'hello.txt'}, ExpiresIn = 100)
        
        
        # Create a URL valid for 60 seconds.
        return s3Client.generate_presigned_url('get_object',
                                               Params={'Bucket': AWS_STORAGE_BUCKET_NAME,'Key': kwargs['filepath']},
                                               ExpiresIn=60)

    def get(self, request, *args, **kwargs):
        instance=request.user.userprofile
        #m = get_object_or_404(UserProfile)
        m = instance
       # u = request.user
        
        
        
        #if u.is_authenticated() and (u.get_profile().is_very_special() or u.is_staff):
        if request.user.is_authenticated:    
            if m.image:
                #filepath = MEDIA_URL + 'yourspace/%s/profile_pics/%s/' % (instance.user.username, m.image)
                #mykeyname = 'yourspace/%s/profile_pics/%s/' % (instance.user.username, m.image)
                filepath =  '%s' % (m.image)
                #filepath = MEDIA_URL + '%s' % (m.image)
                url = self.get_redirect_url(filepath=filepath)
                # The below is taken straight from RedirectView.
                if url:
                    if self.permanent:
                        return http.HttpResponsePermanentRedirect(url)
                    else:
                        return http.HttpResponseRedirect(url)
                else:
                    logger.warning('Gone: %s', self.request.path,
                                extra={
                                    'status_code': 410,
                                    'request': self.request
                                })
                    return http.HttpResponseGone()
            else:
                raise http.Http404
        else:
            raise http.Http404


class MyTestView(TemplateView):
    template_name = './test.html'

    
    def get(self, request):
           
        p_form = UserProfileForm(instance=request.user.userprofile)
        print(p_form)
        print("I just printed p_form")
                
        args = {'user': request.user, 'p_form': p_form}
        print(args)
        print("I just printed args")
        #args = {'user': request.user, 'gallery_plots' : gallery_plots, 'plots2show' : plots2show}
        
        #return render(request, self.template_name, args)
        gallery_plots=Gallery_Plots.objects.filter(user=request.user)
        
        plots2show = Gallery_Plots.objects.filter(user=request.user).order_by('-myDate')[0:2]
        
        args = {'user': request.user, 'p_form': p_form, 'gallery_plots' : gallery_plots, 'plots2show' : plots2show}
        #args = {'user': request.user, 'gallery_plots' : gallery_plots, 'plots2show' : plots2show}
        
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
                return redirect('test')
            
            args = {'user': request.user,'p_form':p_form}
                
            return render(request, self.template_name, args) 


            
            
class Profile(TemplateView):
    template_name = './profile.html'

    
    def get(self, request):
           
        p_form = UserProfileForm(instance=request.user.userprofile)
        
        gallery_plots=Gallery_Plots.objects.filter(user=request.user)
        
        plots2show = Gallery_Plots.objects.filter(user=request.user).order_by('-myDate')[0:2]
        
        args = {'user': request.user, 'p_form': p_form, 'gallery_plots' : gallery_plots, 'plots2show' : plots2show}
        #args = {'user': request.user, 'gallery_plots' : gallery_plots, 'plots2show' : plots2show}
        
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
        tracking_data=Tracking_Data.objects.filter(user=request.user)
        
       # myfilename=graph_data.graph_filename
       # mydate=graph_data.myDate
        return render(request, self.template_name, 
                      {'graph_data' : graph_data, 'tracking_data' : tracking_data})
        

class DeleteView(TemplateView):
    template_name = './projects.html'
  
#if request.method == 'POST': # If the form has been submitted...
    def get(self,request,safekey):
    
        if request.user.is_authenticated:
            #raise Http404
            data_row_old=Graph_Data.objects.get(safekey=safekey)
            data_row_old.delete()
            
            return redirect('projects')


class DeletePlotView(TemplateView):
    template_name = './gallery.html'
  
#if request.method == 'POST': # If the form has been submitted...
    def get(self,request,pk):
    
        if request.user.is_authenticated:
            #raise Http404
            plot_row_old=Gallery_Plots.objects.get(pk=pk)
            plot_row_old.delete()
            
            return redirect('gallery')        
        



   
    
class HomeView(TemplateView):
    template_name = './bubblechart.html' 
    
    
    def get(self,request):
        
        myXlist='1,2'
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
        
        
        
        form = HomeForm()
        formplot = GalleryForm()
                       
        plotdict , plot =bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,myScale)
        
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
                    #repeat=Graph_Data.objects.get(graph_filename=myfilename)
                    repeat=Graph_Data.objects.filter(user=request.user).get(graph_filename=myfilename)
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
                myXlist=np.array(myXlist, dtype=np.float32)
                myYdata=form.cleaned_data['myY']
                myYlist=myYdata.split(",")
                myYlist=np.array(myYlist, dtype=np.float32)
                myRdata=form.cleaned_data['myRadius']
                myRlist=myRdata.split(",")
                myRlist=np.array(myRlist, dtype=np.float32)
                myScale=form.cleaned_data['myScale']
#                
                print('HELLO AGAIN')    
                    #scale = 10
                plotdict, plot =bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,myScale)
                
                print('HELLO The Third Time')
                
                #myname = request.POST.get('name')
                #print(myname)
                #myaction = request.POST.get('action')
                #print(myaction)
                #if myname == 'make_png'or myaction=='make_png':
                    #print('I am infront of the if statement')
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
                mypkRadius=myRdata
                
                dict2={"form":form,"formplot":formplot,"mypkX":mypkX,"mypkY":mypkY,"mypkRadius":mypkRadius}
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
    
    
    def get(self,request,safekey):
        if request.user.is_authenticated:
#        #        graph_data=Graph_Data.objects.get(pk=self.kwargs.get('pk'))
            
            formplot = GalleryForm()
            graph_data=Graph_Data.objects.get(safekey=safekey)
            print(safekey)
            pk=graph_data.pk
            print(pk)
            #graph_data=Graph_Data.objects.get(pk=pk)
            mypkX=graph_data.myX
            mypkY=graph_data.myY
            mypkRadius=graph_data.myRadius
        
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
            myXlist=np.array(myXlist, dtype=np.float32)
            myYdata=graph_data.myY
            myYlist=myYdata.split(",")
            myYlist=np.array(myYlist, dtype=np.float32)
            myRdata=graph_data.myRadius
            myRlist=myRdata.split(",")
            myRlist=np.array(myRlist, dtype=np.float32)
            myScale=graph_data.myScale
            
#            
            
            #scale = 10
            plotdict, plot =bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,myScale)
            dict2={"form":form,"formplot":formplot,"mypkX":mypkX,"mypkY":mypkY,"mypkRadius":mypkRadius}
            dict3={**plotdict , **dict2}
                

 
        #form = HomeForm(request.POST)

            
        return render(request, self.template_name, dict3)
   
    
    
    def post(self,request,safekey):
    #if request.method == 'POST': # If the form has been submitted...
        if request.user.is_authenticated:

            #raise Http404
            
            instance = get_object_or_404(Graph_Data, safekey=safekey)
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
                    #repeat=Graph_Data.objects.get(graph_filename=myfilename)
                    repeat=Graph_Data.objects.filter(user=request.user).get(graph_filename=myfilename)
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
                myXlist=np.array(myXlist, dtype=np.float32)
                myYdata=form.cleaned_data['myY']
                myYlist=myYdata.split(",")
                myYlist=np.array(myYlist, dtype=np.float32)
                myRdata=form.cleaned_data['myRadius']
                myRlist=myRdata.split(",")
                myRlist=np.array(myRlist, dtype=np.float32)
                myScale=form.cleaned_data['myScale']
                    
                    #scale = 10
                plotdict, plot=bubbleplot(mytitle, myXlabel, myYlabel,myXlist, myYlist,myRlist,myScale)
                
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
                mypkRadius=myRdata
                
                dict2={"form":form,"formplot":formplot,"mypkX":mypkX,"mypkY":mypkY,"mypkRadius":mypkRadius}
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
