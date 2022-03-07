from buscas.extrator_iq.extract import ExtratorMysql, AnaltyChances, ExtracToDjango
from buscas.models import Paridade, Configuração, Chance, Vela, analyVelas
from datetime import datetime, timedelta
import time

def init():
    config = Configuração.objects.filter()[0]
    ex = ExtratorMysql(config.login, config.senha)
    return ex

#========================================== Darly ====================================================================================
def deleteVelasBefore():
    print('\n - Iniciando exclusão de velas antigas')
    days_exclude = Configuração.objects.filter()[0].dias_salvos
    days_exclude = days_exclude + (2*(days_exclude//7)) + 2
    day_delete = datetime.today() - timedelta(days=days_exclude)
    velas_before = Vela.objects.filter(data__lte=day_delete)
    velas_before.delete()
    print('     Exclusão de velas concluida com sucesso!\n')

def extractStand(tipo, timeframe):
    config = Configuração.objects.filter()[0]
    ex = ExtracToDjango(config.login, config.senha)
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')

    for par in Paridade.objects.filter():
        par = par.name
        datas = ex.pipeline(tipo, par)
        for data in datas:
            Vela.objects.create(par=par, data=data['date'], timeframe=timeframe, direc=data['direc'], hora=data['hora'], minuto=data['minuto'])
    del ex

def extract_1_1_Django():
    print('Iniciando extração vela 1 1')
    extractStand('1 1', 1)

def extract_1_2_Django():
    extractStand('1 2', 1)

def extract_5_Django():
    extractStand('5', 5)

def extract_15_Django():
    extractStand('15', 15)


def all_dairly_task():
    print('Iniciando tarefaz diarias')
    deleteVelasBefore()
    extract_1_2_Django()
    extract_5_Django()
    extract_15_Django()
    print('     Finalizando tarefaz diarias')


#========================================== Creat chances ======================================================================================

def extractAllDjango():
    print('Iniciando extração de velas')
    config = Configuração.objects.filter()[0]
    ex = ExtracToDjango(config.login, config.senha)
    ex.DAYS_EXTRACT = config.dias_salvos
    Vela.objects.all().delete()

    tipos = ['5 all', '15 all']
    tipos_dic = {'1 all':1, '5 all':5, '15 all':15}

    for tipo in tipos:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
        for par in Paridade.objects.filter():
            time.sleep(1)
            par = par.name
            datas = ex.pipeline(tipo, par)
            for data in datas:
                Vela.objects.create(par=par, data=data['date'], timeframe=tipos_dic[tipo], direc=data['direc'], hora=data['hora'], minuto=data['minuto'])
                
    print('     Finalizado Extração completa de velas')


def sumDirectionsDjango():
    print('Iniciando criação de Chances por Velas')
    time_frames = ['5', '15']
    horas = [n for n in range(0,24)]
    config = Configuração.objects.filter()[0]
    qtd_days = config.dias_salvos
    Chance.objects.all().delete()

    for timeframe in time_frames:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {timeframe}')
        for hora in horas:
            print(f'{timeframe} - Hora {hora}')
            minutos = [n for n in range(0 ,60, int(timeframe))]
            for minuto in minutos:
                for par in Paridade.objects.filter():
                    par = par.name
                    direc, call, sell, taxa = analyVelas(par, timeframe, hora, minuto, qtd_days)
                    if direc:
                        Chance.objects.create(par=par, timeframe=timeframe, hora=hora, minuto=minuto, call=call, sell=sell, porcent=taxa, direc=direc)

    print('     Finalização de criação de Chances')


def ResetValues():
    print('Iniciando Reset de Velas')
    extractAllDjango()
    sumDirectionsDjango()

#========================================== Extract Myslq ====================================================================================

def extractAllMysql():
    ex = init()
    tipos = ['5 all','15 all']
    for tipo in tipos:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
        for par in Paridade.objects.filter():
            ex.setBanco(par.name)
            ex.pipeline(tipo, par.name)
        del ex


def sumDirectionsMysql():
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
                    par = par.name
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


