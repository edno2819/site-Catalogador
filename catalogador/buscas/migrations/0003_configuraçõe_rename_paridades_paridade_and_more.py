# Generated by Django 4.0.2 on 2022-02-24 18:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscas', '0002_configurações_paridades'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuraçõe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dias_Salvos', models.PositiveIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.RenameModel(
            old_name='Paridades',
            new_name='Paridade',
        ),
        migrations.DeleteModel(
            name='Configurações',
        ),
    ]
