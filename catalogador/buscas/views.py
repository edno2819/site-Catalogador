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
        par_ = request.POST.get('par', '0')
        time = int(request.POST.get('time', '0'))
        gale = int(request.POST.get('gale', '0'))


        datas = Chance.objects.filter(par=par_) if par_!='0' else Chance.objects.all() 
        datas = datas.filter(timeframe=time) if time!=0 else datas


        datas = datas.order_by('-porcent','-par')[0:100]

        context.update({'test':request.POST.get('time'), 'chances': datas})
        return render(request, 'result.html', context) 

    return render(request, 'result.html', context) 