from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from dateutil import tz
from banco import MysqlClass
import time


def timestamp_converter(x): 
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]  

class IqOption:        
    def conect(self, conta, senha):
        self.API = IQ_Option(conta, senha)
        self.API.connect()
        self.type ='PRACTICE'
        
        if self.API.check_connect(): 
            return True
        else: 
            return False


    def reconnect(self):
        if not self.API.check_connect(): 
            self.API.connect()
            self.API.change_balance(self.type)
            return self.API.check_connect()


    def change_balance(self, type='PRACTICE'):
        '''PRACTICE / REAL'''
        self.type = type
        self.API.change_balance(type)
        

    def get_velas(self, par, step:int, time_frame:int):
        result=[]
        velas = self.API.get_candles(par, time_frame*60, step+1, time.time())
        for vela in velas:
            direct= (1 if vela['open']<vela['close'] else -1) if vela['open']!=vela['close'] else 0
            vela_convert=[str(timestamp_converter(vela['from'])),vela['open'],vela['max'],vela['min'],vela['close'], direct]
            result.append(vela_convert)
        return result


    def close(self):
        self.API.api.close()

class Extrator:
    TIMES = [1, 5, 15]
    VELAS = {1:1440, 5:288, 15:96}

    def __init__(self, login, senha) -> None:
        host = 'ec2-35-168-80-116.compute-1.amazonaws.com'
        user = 'jfzbjbghuninan'
        database = 'd7gm26lueueuo6'
        password = 'ecadefe331e7876b479ceb4acdb00c95010f37259d36794ea7b3c7d5b0782c0e'
        self.banco = MysqlClass(host, user, password, database)
    
        self.iq = IqOption()
        self.iq.conect(login, senha)

    def setBanco(self, asset):
        query = f'''CREATE TABLE IF NOT EXISTS {asset} (
                                                        Date varchar(32),
                                                        time_vela int(2)
                                                        direcao varchar(32)
                                                        hora int(2)
                                                        minuto int(2)
                                                        )'''
        self.banco.execute(query)
        self.banco.commit()




    def checkConect(self):
        pass
    
    def GetVelas(self, par, time):
        values = self.iq.get_velas(par, 1000, time)
        return values


if __name__ == '__main__':
    iq = Extrator('edno28@hotmail.com', '99730755ed')
    par = 'EURUSD'
    time = 1
    a = iq.GetVelas()
    print(a)

