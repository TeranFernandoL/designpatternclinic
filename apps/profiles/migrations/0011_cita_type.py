# Generated by Django 2.2.13 on 2020-09-14 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_cita_diagnostico'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='type',
            field=models.CharField(blank=True, choices=[('NORMAL', 'NORMAL'), ('EMERGENCIA', 'EMERGENCIA'), ('DOMICILIO', 'DOMICILIO')], max_length=200, null=True),
        ),
    ]
