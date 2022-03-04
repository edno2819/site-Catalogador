from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from datetime import datetime



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
        return datetime.strptime(f'{self.hora}:{self.minuto}', "%H:%M").__str__()[11:16]

    def __str__(self):
        return f'{self.par}-{self.direc}-{self.porcent}%'
    


# len(Chance.objects.all())
# new = Chance.objects.get(par='GBPCHF', timeframe=15, hora=4, minuto=15)
# new.call = call, new.sell=sell, new.porcent=taxa, new.direc=direc
# new.save()