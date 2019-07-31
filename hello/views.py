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
from bokeh.plotting import figure , curdoc , show , output_file
from bokeh.resources import CDN
from bokeh.embed import components
#from bokeh.models import ColumnDataSource, ColorBar
#from bokeh.palettes import Spectral6
#from bokeh.transform import linear_cmap


from .models import Greeting 
from .forms import HomeForm
from .compute import compute



#class HomeView(TemplateView):
#    template_name = 'home/home.html'
#
#
#    def get(self, request):
#        form = HomeForm()
#
#        args = {
#            'form': form
#        }
#        return render(request, self.template_name, args)
#
#
#    def post(self, request):
#        form = HomeForm(request.POST)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.save()
#
#            text = form.cleaned_data['post']
#            form = HomeForm()
#            return redirect('home:home')
#        
#        args = {'form': form, 'text': text}
#        return render(request, self.template_name, args)    


def index(request):  
    if request.method == 'POST': # If the form has been submitted...
        form = HomeForm(request.POST) # A form bound to the POST data
    
        if form.is_valid():
            postall = form.save(commit=False)
            postall.save()
            form = HomeForm()
            script, div = mainplot(form)
    
    else:
        form = HomeForm()
        plot = figure(plot_width=400, plot_height=400, title="Your title will go here")
        script, div = components(plot, CDN)
    
            
    return render(request, "index.html", {"the_script": script, "the_div": div, "form": form})   




def mainplot(request,form):
    mytitle = form.post
    
    plot = figure(plot_width=400, plot_height=400, title=mytitle)
    plot.circle([1,2,3], [3,4,7])
    
    script2, div2 = components(plot, CDN)
#    curdoc().add_root(plot)
    
    return {"the_script": script2, "the_div": div2} 
    



     
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



def db(request):

   greeting = Greeting()
   greeting.save()

   greetings = Greeting.objects.all()

   return render(request, "db.html", {"greetings": greetings})





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
