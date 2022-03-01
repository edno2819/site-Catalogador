# Generated by Django 4.0.2 on 2022-02-28 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscas', '0009_delete_chance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('par', models.CharField(max_length=32)),
                ('timeframe', models.PositiveSmallIntegerField()),
                ('hora', models.PositiveSmallIntegerField()),
                ('minuto', models.PositiveSmallIntegerField()),
                ('call', models.PositiveSmallIntegerField()),
                ('sell', models.PositiveSmallIntegerField()),
                ('porcent', models.PositiveSmallIntegerField()),
                ('direc', models.CharField(max_length=32)),
            ],
        ),
    ]
