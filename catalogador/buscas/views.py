from buscas.models import Paridade, Chance
from django.shortcuts import render
from datetime import timedelta



def home(request):
    context = {'pares':Paridade.objects.filter()}
    return render(request, 'index.html', context)

def layout(request):
    return render(request, 'layout-static.html') 




def format_chance(datas):
    limit = 500
    chances = []
    for chance in datas[:limit]:
        horario = (timedelta(hours=chance.hora, minutes=chance.minuto) - timedelta(minutes=chance.timeframe)).seconds
        before_hora = horario//3600
        before_minuto = int((horario%3600)/60)
        vela_anterior = Chance.objects.filter(par=chance.par, timeframe=chance.timeframe, hora=before_hora, minuto=before_minuto)
        new = {'horario':chance.formatData(), 'par':chance.par, 'porcent':chance.porcent, 'timeframe':chance.timeframe, 'direc':chance.direc}
        if len(vela_anterior)==1:
            vela_anterior = vela_anterior[0]
            new.update({'horario_before':vela_anterior.formatData(), 'porcent_before':vela_anterior.porcent, 'direc_before':vela_anterior.direc})
        chances.append(new)
    return chances


def busca(request):
    datas = Chance.objects.all().order_by('-porcent','-par')

    chances = format_chance(datas)

    context = {'pares':Paridade.objects.filter(), 'resultado_qtd':len(datas), 'chances':chances}

    if request.method == "POST":
        par_ = request.POST.get('par', '0')
        time = int(request.POST.get('time', '0'))

        datas = Chance.objects.filter(par=par_) if par_!='0' else Chance.objects.all() 
        datas = datas.filter(timeframe=time) if time!=0 else datas
        datas = datas.order_by('-porcent','-par')

        chances = format_chance(datas)

        context.update({'chances': chances, 'resultado_qtd':len(datas)})
        return render(request, 'result.html', context) 

    return render(request, 'result.html', context) 