from django.shortcuts import render
from django.http import HttpResponse

#from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import InputForm
from .compute import compute

import requests

from .models import Greeting

# Create your views here.
#def index(request):
    # return HttpResponse('Hello from Python!')
 #   return render(request, "index.html")
 
 
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    print('Hello Niki World')
    #return HttpResponse('<pre>' + r.text + '</pre>' + 'Hello Niki World')

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            return present_output(form)
    else:
        form = InputForm()

    context = {'form': form}

    return render(request,'hw1.html',context)




def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def present_output(form):
    r = form.r
    s = compute(r)
    return HttpResponse('Hello, World again! sin(%s)=%s' % (r, s))
