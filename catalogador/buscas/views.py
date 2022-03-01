from django.views.generic.edit import CreateView
from buscas.models import Paridade, Chance
from django.shortcuts import render


def home(request):
    context = {'pares':Paridade.objects.filter()}
    return render(request, 'index.html', context)

def layout(request):
    return render(request, 'layout-static.html') 

def busca(request):
    context = {'pares':Paridade.objects.filter()}

    if request.method == "POST":
        datas = Chance.objects.filter().order_by('-par').order_by('-porcent')
        context.update({'test':request.POST.get('time'), 'chances': datas})
        return render(request, 'result.html', context) 

    return render(request, 'result.html', context) 