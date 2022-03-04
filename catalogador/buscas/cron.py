from buscas.extrator_iq.extract import ExtratorMysql, AnaltyChances
from buscas.models import Paridade, Configuraçõe, Chance
from datetime import datetime

def init():
    config = Configuraçõe.objects.filter()[0]
    ex = ExtratorMysql(config.login, config.senha)
    return ex


def sumDirections():
    time_frames = ['5','15']
    horas = [n for n in range(0,23)]
    ana = AnaltyChances()    
    Chance.objects.all().delete()

    for timeframe in time_frames:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {timeframe}')
        for hora in horas:
            minutos = [n for n in range(0 ,60, int(timeframe))]
            for minuto in minutos:
                for par in Paridade.objects.filter():
                    datas = ana.getDatas(par, hora, minuto, timeframe, 10)
                    if len(datas)!=0:
                        direc, call, sell, taxa = ana.formatChance(datas)
                        print(par, timeframe, hora, minuto, call, sell, taxa, direc)
                        Chance.objects.create(par=par, timeframe=timeframe, hora=hora, minuto=minuto, call=call, sell=sell, porcent=taxa, direc=direc)
                        
    '''
    - Preparar a exclusão de dados
    - Tratar quando não houver dados suficientes no tempo passado
    '''
    print('Atualização de chances concluida com sucesso!')


def extract_all():
    ex = init()
    tipos = ['5 all','15 all']
    for tipo in tipos:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
        for par in Paridade.objects.filter():
            ex.setBanco(par.name)
            ex.pipeline(tipo, par.name)
        del ex


def extract_1_1():
    ex = init()
    tipo = '1 1'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        try:
            ex.pipeline(tipo, par.name)
        except Exception as e: 
            print(f'{par.name} - Erro '+ str(e))
    del ex

def extract_1_2():
    ex = init()
    tipo = '1 2'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        try:
            ex.pipeline(tipo, par.name)
        except Exception as e: 
            print(f'{par.name} - Erro '+ str(e))
    del ex

def extract_5():
    ex = init()
    tipo = '5'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        try:
            ex.pipeline(tipo, par.name)
        except Exception as e: 
            print(f'{par.name} - Erro '+ str(e))
    del ex

def extract_15():
    ex = init()
    tipo = '15'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        try:
            ex.pipeline(tipo, par.name)
        except Exception as e: 
            print(f'{par.name} - Erro '+ str(e))
    del ex


