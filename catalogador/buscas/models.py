from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator



class Post(models.Model):
    title = models.CharField(max_length=200)
    resumo = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Paridade(models.Model):
    name = models.CharField(max_length=6, null=False, blank=False,
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
        return f'Dias Salvos no banco: {self.dias_salvos}'