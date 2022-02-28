from django.views.generic.edit import CreateView
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')

def layout(request):
    return render(request, 'layout-static.html') 

def busca(request):
    return render(request, 'result.html', {'test':'menssagem de text'}) 