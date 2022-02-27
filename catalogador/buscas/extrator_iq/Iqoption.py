from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from dateutil import tz
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

        
    def bet_binaria(self, par:str, amount:float, action:str, time_frame:int, func=''):
        status, id = self.API.buy(amount, par, action, time_frame)
        func(status, action) if func!='' else ...

        if status:
            status2,lucro=self.API.check_win_v4(id)
            if status2:
                return round(lucro, 2)
        else: return False
        

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