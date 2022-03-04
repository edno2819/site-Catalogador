from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from datetime import datetime
from buscas.extrator_iq.extract import ExtracToDjango
from django.contrib import admin
from django.utils.html import format_html




class Paridade(models.Model):
    name = models.CharField(max_length=6, null=False, blank=False, unique=True,
    validators=[RegexValidator('^[A-Z_]*$',
                               'Apenas Letras maiúsculas permitidas')])

    def __str__(self):
        return self.name


class Configuraçõe(models.Model):
    login = models.CharField(max_length=32, null=False, blank=False)
    senha = models.CharField(max_length=32, null=False, blank=False)
    dias_salvos = models.PositiveIntegerField(default=10, null=False, blank=False,
            validators=[
                MaxValueValidator(50),
                MinValueValidator(1)
            ])

    def __str__(self):
        return f'Login: {self.login}  | Dias Salvos: {self.dias_salvos}'


class Chance(models.Model):
    direc_choices = (("CALL", "COMPRA" ), ('SELL', 'VENDA'))
    time_choices = ((1, '1'), (5, '5'), (15, '15'))

    par = models.CharField(max_length=32)
    timeframe = models.PositiveSmallIntegerField(choices=time_choices, null=False, blank=False)
    hora = models.PositiveSmallIntegerField(null=False, blank=False)
    minuto = models.PositiveSmallIntegerField(null=False, blank=False)
    call = models.PositiveSmallIntegerField(null=False, blank=False)
    sell = models.PositiveSmallIntegerField(null=False, blank=False)
    porcent = models.PositiveSmallIntegerField(null=False, blank=False)
    direc = models.CharField(max_length=32, choices=direc_choices,  null=False, blank=False)

    # class Meta:
    #     unique_together = (('par', 'timeframe', 'hora', 'minuto'),)
        
    def formatData(self):
        self.horario = datetime.strptime(f'{self.hora}:{self.minuto}', "%H:%M").__str__()[11:16]
        return self.horario

    def __str__(self):
        return f'{self.par}-{self.direc}-{self.porcent}%'
    

class Vela(models.Model):
    direc_choices = (("CALL", "COMPRA" ), ('SELL', 'VENDA'))
    time_choices = ((1, '1'), (5, '5'), (15, '15'))

    par = models.CharField(max_length=32)
    data = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
    timeframe = models.PositiveSmallIntegerField(choices=time_choices, null=False, blank=False)
    hora = models.PositiveSmallIntegerField(null=False, blank=False)
    minuto = models.PositiveSmallIntegerField(null=False, blank=False)
    direc = models.CharField(max_length=32, choices=direc_choices,  null=False, blank=False)
        
    @admin.display(boolean=False)
    def Horário(self):
        self.horario = datetime.strptime(f'{self.hora}:{self.minuto}', "%H:%M").__str__()[11:16]
        return self.horario


    @admin.display(ordering='direc')
    def Direção(self):
        color = 'a71c1c' if self.direc=='SELL' else '319c35'
        return format_html(
            '<span style="color: #{};">{}</span>',
            color,
            self.direc,
        )

    def __str__(self):
        return f'{self.data}-{self.par}-{self.timeframe}-{self.direc}'


#========================================== functions =======================================================================

def analyVelas(par, timeframe, hora, minuto, limit=10):
    datas = Vela.objects.filter(par=par, timeframe=timeframe, hora=hora, minuto=minuto).order_by('-data')[:limit]
    result = {'CALL':0, 'SELL':0}
    for data in datas:
        if data.direc=='CALL':
            result['CALL'] += 1
        else:
            result['SELL'] += 1

    if result['CALL']==0 and result['CALL']==0:
        return False, False, False, False
    
    direc, maxi = ('CALL', result['CALL']) if result['CALL']>result['SELL']  else ('SELL', result['SELL'])  
    taxa = int((100*maxi)/(result['CALL']+result['SELL']))
    return direc, result['CALL'], result['SELL'], taxa


# def sumDirectionsVelas():
#     time_frames = ['5','15']
#     horas = [n for n in range(0,24)]
#     #Chance.objects.all().delete()

#     for timeframe in time_frames:
#         print(f'{datetime.now().strftime("%H-%M-%S %d/%m/%Y")} - Tipo {timeframe}')
#         for hora in horas:
#             print(f'{timeframe} - Hora {hora}')
#             minutos = [n for n in range(0 ,60, int(timeframe))]
#             for minuto in minutos:
#                 for par in Paridade.objects.filter():
#                     par = par.name
#                     direc, call, sell, taxa = analyVelas(par, timeframe, hora, minuto, 10)
#                     if direc:
#                         Chance.objects.create(par=par, timeframe=timeframe, hora=hora, minuto=minuto, call=call, sell=sell, porcent=taxa, direc=direc)

#     print('Finalização de creação de Chances por Velas')


# #extractAllDjango()
# sumDirectionsVelas()

# from datetime import timedelta

# datas = Chance.objects.filter(par='EURUSD', timeframe=5, hora=13)
# chances = []
# for chance in datas:
#     horario = (timedelta(hours=chance.hora, minutes=chance.minuto) - timedelta(minutes=chance.timeframe)).seconds
#     before_hora = horario//3600
#     before_minuto = int((horario%3600)/60)
#     vela_anterior = Chance.objects.filter(par=chance.par, timeframe=chance.timeframe, hora=before_hora, minuto=before_minuto)
#     new = {'horario':chance.formatData(), 'par':chance.par, 'porcent':chance.porcent, 'timeframe':chance.timeframe, 'direc':chance.direc}
#     if len(vela_anterior)==1:
#         vela_anterior = vela_anterior[0]
#         new.update({'horario_before':vela_anterior.formatData(), 'porcent_before':vela_anterior.porcent, 'direc_before':vela_anterior.direc})
#     chances.append(new)
