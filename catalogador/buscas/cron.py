from buscas.extrator_iq.extract import ExtracToDjango
from buscas.models import Paridade, Configuração, Chance, Vela, analyVelas
from datetime import datetime, timedelta
import time


#========================================== Darly ====================================================================================
def deleteVelasBefore():
    print('\n - Iniciando exclusão de velas antigas')
    days_exclude = Configuração.objects.filter()[0].dias_salvos
    days_exclude = days_exclude + (2*(days_exclude//7)) + 2
    day_delete = datetime.today() - timedelta(days=days_exclude)
    velas_before = Vela.objects.filter(data__lte=day_delete)
    velas_before.delete()
    print('     Exclusão de velas concluida com sucesso!\n')


def sumDirectionsDjango():
    print('     Iniciando criação completa de Chances')
    time_frames = ['1', '5', '15']
    horas = [n for n in range(0,24)]
    config = Configuração.objects.filter()[0]
    qtd_days = config.dias_salvos
    print('    Deletando todas as Chances!')
    Chance.objects.all().delete()

    for timeframe in time_frames:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {timeframe}')
        for hora in horas:
            minutos = [n for n in range(0 ,60, int(timeframe))]
            for minuto in minutos:
                for par in Paridade.objects.filter():
                    par = par.name
                    direc, call, sell, taxa = analyVelas(par, timeframe, hora, minuto, qtd_days)
                    if direc:
                        try:
                            Chance.objects.create(par=par, timeframe=timeframe, hora=hora, minuto=minuto, call=call, sell=sell, porcent=taxa, direc=direc)
                        except:
                            print('Erro no inserção de chances no banco')

    print('     Finalização de criação de Chances')


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
    sumDirectionsDjango()
    print('     Finalizando tarefaz diarias')


#========================================== Creat chances ======================================================================================

def extractAllDjango():
    print('     Iniciando extração completa de velas')
    config = Configuração.objects.filter()[0]
    ex = ExtracToDjango(config.login, config.senha)
    ex.DAYS_EXTRACT = config.dias_salvos
    print('     Deletando todas as velas!')
    Vela.objects.all().delete()

    tipos = ['1 all', '5 all', '15 all']
    tipos_dic = {'1 all':1, '5 all':5, '15 all':15}

    for tipo in tipos:
        print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
        for par in Paridade.objects.filter():
            time.sleep(1)
            par = par.name
            datas = ex.pipeline(tipo, par)
            for data in datas:
                try:
                    Vela.objects.create(par=par, data=data['date'], timeframe=tipos_dic[tipo], direc=data['direc'], hora=data['hora'], minuto=data['minuto'])
                except:
                    print('Erro no inserção de Velas no banco')
                    
    print('     Finalizado Extração completa de velas')


def ResetValues():
    print('Iniciando Reset de Velas')
    extractAllDjango()
    sumDirectionsDjango()

