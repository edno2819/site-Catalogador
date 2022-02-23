from django.shortcuts import render
from django.views.generic.edit import CreateView

def home(request):
    return render(request, 'index.html')

def layout(request):
    return render(request, 'layout-static.html') 