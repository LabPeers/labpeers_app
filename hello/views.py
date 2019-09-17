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
from django.shortcuts import render 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from bokeh.plotting import figure , curdoc , show , output_file
from bokeh.resources import CDN
from bokeh.embed import components
import pandas as pd
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter, HoverTool
from bokeh.palettes import Viridis256
from bokeh.transform import transform

#from bokeh.models import ColumnDataSource, ColorBar
#from bokeh.palettes import Spectral6
#from bokeh.transform import linear_cmap


#from .models import Greeting 
#from .models import Graph_Data
from .forms import HomeForm
from .compute import compute
from django.contrib.auth.models import User



class HomeView(TemplateView):
    template_name = './home.html' 
    
    
    def get(self,request):
        
        form = HomeForm()
        users = User.objects.exclude(id=request.user.id)
        plot = figure(plot_width=400, plot_height=400, title='Outside function')
        script, div = components(plot, CDN) 
        return render(request, self.template_name, {"users": users, "the_script": script, "the_div": div, "form": form})
    
    
    def post(self,request):
    #if request.method == 'POST': # If the form has been submitted...
        form = HomeForm(request.POST) # A form bound to the POST data
    
    
        if form.is_valid():
            
            #form.save()
            form.save()
            mytitle=form.cleaned_data['graph_title']
            myXdata=form.cleaned_data['myX']
            myXlist=myXdata.split(",")
            myYdata=form.cleaned_data['myY']
            myYlist=myYdata.split(",")
            myRdata=form.cleaned_data['myRadius']
            myRlist=myRdata.split(",")
#            
            
            #scale = 10
            d = {'myXaxis': myXlist, 'myYaxis': myYlist,'myBubble': myRlist} 

            df = pd.DataFrame(data = d)
            source = ColumnDataSource(df)
            plot = figure(plot_width=400, plot_height=400, title=mytitle)

            color_mapper = LinearColorMapper(palette = Viridis256, low = df['myBubble'].min(), high = df['myBubble'].max())
            color_bar = ColorBar(color_mapper = color_mapper,
                                 location = (0, 0),
                                 ticker = BasicTicker())
            plot.add_layout(color_bar, 'right')
            plot.scatter(x = 'myXaxis', y = 'myYaxis', size = 'myBubble', legend = None, fill_color = transform('myBubble', color_mapper), source = source)
            plot.add_tools(HoverTool(tooltips = [('Count', '@count')]))

            
            script, div = components(plot, CDN)            
            
            
#            graph_title.user = request.user
#            graph_title.save()

#            mytitle = form.cleaned_data['graph_title']

            #postall.save()
            
           #script, div = mainplot(form)            #form.save(commit=False)

            #mytitle = form.post
            
            #mytitle = Graph_title.objects.all()
            
      

 
            form = HomeForm()
            
            #form=HomeForm()
            
        return render(request, self.template_name, {"the_script": script, "the_div": div, "form": form})
        #return render(request, self.template_name, {"form": form})

            #print form.cleaned_data['my_form_field_name']

#            return HttpResponseRedirect('/thanks/') # Redirect after POST
    
#    else:
#        form = HomeForm()
#        plot = figure(plot_width=400, plot_height=400, title="Your title will go here2")
#        script, div = components(plot, CDN)
    
            




# =============================================================================
# def db(request):
# 
#    greeting = Greeting()
#    greeting.save()
# 
#    greetings = Greeting.objects.all()
# 
#    return render(request, "db.html", {"greetings": greetings})
# 
# =============================================================================


# =============================================================================
# def mainplot(request,form):
#     #mytitle = form.post
#     mytitle = "Now it works"
#     plot = figure(plot_width=400, plot_height=400, title=mytitle)
#     plot.circle([1,2,3], [3,4,7])
#     
#     script2, div2 = components(plot, CDN)
# #    curdoc().add_root(plot)
#     
#     return {"the_script": script2, "the_div": div2} 
# =============================================================================
    



     
#        
# =============================================================================
#     if request.method == 'POST':
#         form2 = InputForm2(request.POST)
#         if form2.is_valid():
#             form2 = form2.save(commit=False)
#             plot = figure()
#             plot.circle(form2, form2)
#             script, div = components(plot, CDN)
#             return present_plot(form2)
#             
#             
#     else:
#         form2 = InputForm2() 
#         plot = figure()
#         plot.circle([1,2], [3,4])
#         script, div = components(plot, CDN)
# =============================================================================
        
        
   


# =============================================================================
# def present_output(form):
#     r = form.r
#     s = compute(r)
#     x = form.x
#     t = compute(x)
#     return HttpResponse('Hello, World! sin(%s)=%s' % (r, s))
# =============================================================================





# =============================================================================
# from bokeh.plotting import figure
# from bokeh.io import output_file, show
# 
# def index(request):
# 
#     fg=figure(x_axis_label="x_axis", y_axis_label="y_axis")
# 
#     x=[1,2,3,4]
#     y=[1,2,3,4]
# 
#     fg.circle(x,y)
# 
#     output_file('test_plot.html')
#     return show(fg)
# =============================================================================
 
# =============================================================================
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# 
# from io import BytesIO
# import base64
#  
#  
# def myplot(request):
#     buf = BytesIO()
#     plt.savefig(buf, format='png', dpi=300)
#     image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
#     buf.close()
#     return render(request,'hw1.html',context)
# =============================================================================


# =============================================================================
# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     print('Hello Niki World')
#     #return HttpResponse('<pre>' + r.text + '</pre>' + 'Hello Niki World')
# 
#     if request.method == 'POST':
#         form = InputForm(request.POST)
#         if form.is_valid():
#             form = form.save(commit=False)
#             return present_output(form)
#     else:
#         form = InputForm()
# 
#     context = {'form': form}
# 
#     return render(request,'hw1.html',context)
# 
# =============================================================================




# =============================================================================
# def present_output(form):
#     r = form.r
#     s = compute(r)
#     return HttpResponse('Hello, World again! sin(%s)=%s' % (r, s))
# 
# =============================================================================
