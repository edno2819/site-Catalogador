from buscas.extrator_iq.extract import ExtratorMysql, AnaltyChances
from buscas.models import Paridade, Configuraçõe, Chance
from datetime import datetime

def init():
    config = Configuraçõe.objects.filter()[0]
    ex = ExtratorMysql(config.login, config.senha)
    return ex


def sumDirections():
    time_frames = ['1', '5', '15']
    horas = [n for n in range(0,24)]
    minutos = [n for n in range(1,60)]

    config = Configuraçõe.objects.filter()[0]
    ana = AnaltyChances(config.login, config.senha)    


    for timeframe in time_frames:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {timeframe}')
        for hora in horas:
            for minuto in minutos:
                for par in Paridade.objects.filter():
                    datas = ana.getDatas(par, hora, minuto, timeframe)
                    direc, call, sell, taxa = ana.formatChance(datas)
                    instan = Chance(par, timeframe, hora, minuto, call, sell, taxa, direc)
                    instan.save()
    '''
    - Verificar a entradas dos dados
    - retorna de ana call e sell
    - Quando tiver apenas 1 tipo botar 0 no outro
    - Preparar a exclusão de dados
    - Tratar quando não houver dados suficientes no tempo passado'''



    print('Atualização de chances concluida com sucesso!')


def extract_1_1():
    ex = init()
    tipo = '1 1'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        ex.pipeline(tipo, par.name)
    del ex

def extract_1_2():
    ex = init()
    tipo = '1 2'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        ex.pipeline(tipo, par.name)
    del ex

def extract_5():
    ex = init()
    tipo = '5'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        ex.pipeline(tipo, par.name)
    del ex

def extract_15():
    ex = init()
    tipo = '15'
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for par in Paridade.objects.filter():
        ex.setBanco(par.name)
        ex.pipeline(tipo, par.name)
    del ex


