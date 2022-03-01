from buscas.models import Paridade, Configuraçõe, Chance
from buscas.extrator_iq.extract import Extrator
from datetime import datetime
import logging

log = logging.getLogger(__name__)

def init():
    config = Configuraçõe.objects.filter()[0]
    ex = Extrator(config.login, config.senha)
    return ex


def sumDirections():
    tipos = ['1', '5', '15']
    ex = init()
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {tipo}')
    for tipo in tipos:
        for par in Paridade.objects.filter():
            Chance.query('''
            SELECT direcao from {par} 
            WHERE time_vela={tipo}''')

    print('Atualização de chances concluida com sucesso!')

def teste():
    print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} ')
    ex = init()
    ex.teste()

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


