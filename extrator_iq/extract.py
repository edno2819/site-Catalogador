
from banco import DataBaseClass
from Iqoption import IqOption
from datetime import datetime, timedelta

class Extrator:
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
            direcao = 'CALL' if data[-1]==1 else 'PUT'
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
        datas = self.formattingToDatabase(datas, time)
        self.setBanco(par)
        self.insetRows(datas, par)





if __name__ == '__main__':
    iq = Extrator('edno28@hotmail.com', '99730755ed')
    par = 'EURUSD'
    iq.pipeline('1 1', par)
