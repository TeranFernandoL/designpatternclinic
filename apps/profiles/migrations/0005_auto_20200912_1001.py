# Generated by Django 2.2.13 on 2020-09-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20200912_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medico',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='cedula',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='cedula',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='prefijo',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='telefono',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='usuario',
        ),
        migrations.AddField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='cedula',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
