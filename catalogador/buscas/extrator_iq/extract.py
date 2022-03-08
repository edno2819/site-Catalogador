from buscas.extrator_iq.banco_myslq import MysqlClass
from buscas.extrator_iq.banco import DataBaseClass
from buscas.extrator_iq.Iqoption import IqOption
from datetime import datetime, timedelta


# from banco_myslq import MysqlClass
# from banco import DataBaseClass
# from Iqoption import IqOption
# from datetime import datetime, timedelta

class ExtratorPostGres:
    TIMES = [1, 5, 15]
    VELAS = {1:1500, 5:300, 15:100}

    def __init__(self, login, senha) -> None:
        host = 'ec2-35-168-80-116.compute-1.amazonaws.com'
        user = 'jfzbjbghuninan'
        database = 'd7gm26lueueuo6'
        password = 'ecadefe331e7876b479ceb4acdb00c95010f37259d36794ea7b3c7d5b0782c0e'
        self.banco = DataBaseClass(host, user, password, database)
    

        self.iq = IqOption()
        self.iq.conect(login, senha)
        
    
    def teste(self):
        self.iq.change_balance()
        self.iq.bet_binaria('EURUSD', 1, 'CALL', 1)


    def setVariables(self):
        self.clock_init = 0
        self.clock_end = 12
        self.day_now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.day_before = self.day_now - timedelta(days=1)

    def setBanco(self, asset):
        query = f'''CREATE TABLE IF NOT EXISTS {asset}(
                    date DATE NOT NULL,
                    time_vela SMALLINT NOT NULL,
                    direcao varchar(32) NOT NULL,
                    hora SMALLINT NOT NULL,
                    minuto SMALLINT NOT NULL
                    );'''
        self.banco.cur.execute(query)
        self.banco.commit()

    def filter_data(self):...

    
    def getVelasOneMinute1(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_now and hora>=self.clock_init and hora<self.clock_end:
                datas.append(c)
        return datas

    def getVelasOneMinute2(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before and hora>=self.clock_end:
                datas.append(c)
        return datas

    def getVelasFiveMinute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas

    def getVelas15Minute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas
    
    def insetRows(self, datas, table):
        args_str = ','.join(self.banco.cur.mogrify("(%s,%s,%s,%s,%s)", x).decode("utf-8") for x in datas)
        self.banco.cur.execute(f"INSERT INTO {table} VALUES " + args_str) 


    def formattingToDatabase(self, datas, time_vela):
        lista = []
        for data in datas:
            date = data[0][:10]
            direcao = 'CALL' if data[-1]==1 else 'SELL'
            hora = int(data[0][11:13])
            minuto = int(data[0][14:16])
            row = (date, time_vela, direcao, hora, minuto)
            lista.append(row)
        return lista

    def pipeline(self, tipo, par):
        '''
        1- Check conection IQ
        3- Extract
        4- Prepara os dados
        5- Check conection Database
        6- Set datas to format
        7- Insert datas to Database
        '''
        time = int(tipo.split(' ')[0])
        tipos = {'1 2':self.getVelasOneMinute2, '1 1':self.getVelasOneMinute1, '5':self.getVelasFiveMinute, '15':self.getVelas15Minute}
        datas = tipos[tipo](par, time)
        print(f'     Get data {par}')
        datas = self.formattingToDatabase(datas, time)
        if datas!=[]:
            self.insetRows(datas, par)
        print(f'     Save data {par}')


class ExtratorMysql:
    TIMES = [1, 5, 15]
    VELAS = {1:900, 5:300, 15:100}
    VELAS_ALL = {1:1400, 5:300, 15:100}
    DAYS_EXTRACT = 12


    def __init__(self, login, senha) -> None:
        #mysql://b948f2d03e644f:5e4beba7@us-cdbr-east-05.cleardb.net/heroku_e178f4c06f07972?reconnect=true
        host = 'us-cdbr-east-05.cleardb.net'
        user = 'b948f2d03e644f'
        password = '5e4beba7'
        database = 'heroku_e178f4c06f07972'
        self.banco = MysqlClass(host, user, password, database)


        self.iq = IqOption()
        self.iq.conect(login, senha)
        
    
    def teste(self):
        self.iq.change_balance()
        self.iq.bet_binaria('EURUSD', 1, 'CALL', 1)


    def setVariables(self):
        self.clock_init = 0
        self.clock_end = 12
        self.day_now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.day_before = self.day_now - timedelta(days=1)

    def setBanco(self, asset):
        query = f'''CREATE TABLE IF NOT EXISTS {asset}(
                    date DATE NOT NULL,
                    time_vela SMALLINT NOT NULL,
                    direcao varchar(32) NOT NULL,
                    hora SMALLINT NOT NULL,
                    minuto SMALLINT NOT NULL
                    );'''
        self.banco.execTry(query)
        self.banco.commit()

    def filter_data(self):...

    
    def getVelasOneMinute1(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_now and hora>=self.clock_init and hora<self.clock_end:
                datas.append(c)
        return datas

    def getVelasOneMinute2(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before and hora>=self.clock_end:
                datas.append(c)
        return datas


    def getVelasMinuteAll(self, par, time):
        values = self.iq.getManyVelas(par, self.VELAS_ALL[time]*self.DAYS_EXTRACT, time)
        return values

    def getVelasFiveMinute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas

    def getVelas15Minute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas
    
    def insetRows(self, datas, table):
        args_str = ','.join(str(x) for x in datas)
        self.banco.execTry(f"INSERT INTO {table} VALUES " + args_str) 



    def formattingToDatabase(self, datas, time_vela):
        lista = []
        for data in datas:
            date = data[0][:10]
            direcao = 'CALL' if data[-1]==1 else 'SELL'
            hora = int(data[0][11:13])
            minuto = int(data[0][14:16])
            row = (date, time_vela, direcao, hora, minuto)
            lista.append(row)
        return lista

    def pipeline(self, tipo, par):
        '''
        1- Check conection IQ
        3- Extract
        4- Prepara os dados
        5- Check conection Database
        6- Set datas to format
        7- Insert datas to Database
        '''
        time = int(tipo.split(' ')[0])
        tipos = {
        '1 2':self.getVelasOneMinute2, '1 1':self.getVelasOneMinute1, '5':self.getVelasFiveMinute, '15':self.getVelas15Minute,
        '1 all':self.getVelasMinuteAll, '5 all':self.getVelasMinuteAll, '15 all':self.getVelasMinuteAll
        }

        datas = tipos[tipo](par, time)
        print(f'     Get data {par}')
        datas = self.formattingToDatabase(datas, time)
        if datas!=[]:
            self.insetRows(datas, par)
        print(f'     Save data {par}')


class ExtracToDjango:
    TIMES = [1, 5, 15]
    VELAS = {1:1460, 5:300, 15:100}
    DAYS_EXTRACT = 12


    def __init__(self, login, senha) -> None:
        self.iq = IqOption()
        self.iq.conect(login, senha)


    def setVariables(self):
        self.clock_init = 0
        self.clock_end = 12
        self.day_now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        self.day_before = self.day_now - timedelta(days=1)

    
    def getVelasOneMinute1(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_now and hora>=self.clock_init and hora<self.clock_end:
                datas.append(c)
        return datas


    def getVelasOneMinute2(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            hora = int(c[0][11:13])
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before and hora>=self.clock_end:
                datas.append(c)
        return datas


    def getVelasMinuteAll(self, par, time):
        values = self.iq.getManyVelas(par, self.VELAS[time] * self.DAYS_EXTRACT, time)
        return values

    def getVelasFiveMinute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas

    def getVelas15Minute(self, par, time):
        datas = []
        self.setVariables()
        values = self.iq.get_velas(par, self.VELAS[time], time)
        for c in values:
            obj_date = datetime.strptime(c[0].split(' ')[0], '%Y-%m-%d')
            if obj_date==self.day_before:
                datas.append(c)
        return datas

    def formattingToDatabase(self, datas, time_vela):
        lista = []
        for data in datas:
            date = datetime.strptime(data[0][:10], "%Y-%m-%d")
            direcao = 'CALL' if data[-1]==1 else 'SELL'
            hora = int(data[0][11:13])
            minuto = int(data[0][14:16])
            row = {'date':date, 'timeframe':time_vela, 'direc':direcao, 'hora':hora, 'minuto':minuto}
            lista.append(row)
        return lista

    def pipeline(self, tipo, par):
        time = int(tipo.split(' ')[0])
        tipos = {
        '1 2':self.getVelasOneMinute2, '1 1':self.getVelasOneMinute1, '5':self.getVelasFiveMinute, '15':self.getVelas15Minute,
        '1 all':self.getVelasMinuteAll, '5 all':self.getVelasMinuteAll, '15 all':self.getVelasMinuteAll
        }

        datas = tipos[tipo](par, time)
        print(f'     Get data {par}')
        datas = self.formattingToDatabase(datas, time)
        print(f'     Send data {par}')
        return datas



class AnaltyChances:
    def __init__(self) -> None:
        host = 'us-cdbr-east-05.cleardb.net'
        user = 'b948f2d03e644f'
        password = '5e4beba7'
        database = 'heroku_e178f4c06f07972'
        self.banco = MysqlClass(host, user, password, database)

    def getDatas(self, par, hora, minuto, timeframe, limit=10):
        datas = self.banco.get_data(f'''
                SELECT direcao, COUNT(direcao) FROM {par} 
                WHERE (time_vela={timeframe} and hora={hora} and minuto={minuto})
                GROUP BY direcao
                LIMIT 0, {limit}
                ''') 
        return datas

    def formatChance(self, datas):
        dic = {datas[0][0]:datas[0][1]}

        if len(datas)==1:
            dic.update({'SELL':0}) if  datas[0][0] == 'CALL' else dic.update({'CALL':0})  
        else:
            dic.update({datas[1][0]:datas[1][1]})
                
        direc, maxi = ('CALL', dic['CALL']) if dic['CALL']>dic['SELL']  else ('SELL', dic['SELL'])  
        taxa = int((100*maxi)/(dic['CALL']+dic['SELL']))

        return direc, dic['CALL'], dic['SELL'], taxa



if __name__ == '__main__':
    iq = ExtracToDjango('edno28@hotmail.com', '99730755ed')
    pares = ['EURUSD','GBPCHF']
    for par in pares:
        datas = iq.pipeline('15 all', par)

    # a = AnaltyChances()
    # par = 'GBPCHF'
    # hora=12
    # minuto = 15
    # timeframe = 15

    # datas = a.getDatas(par, hora, minuto, timeframe)
    # a.formatChance(datas)