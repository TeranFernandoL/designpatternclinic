# Generated by Django 2.2.13 on 2020-09-14 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20200914_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta',
            name='medico',
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='paciente',
        ),
        migrations.DeleteModel(
            name='Consultorio',
        ),
        migrations.DeleteModel(
            name='Especialidad',
        ),
        migrations.RemoveField(
            model_name='tratamiento',
            name='consulta',
        ),
        migrations.RemoveField(
            model_name='tratamiento',
            name='medicamento',
        ),
        migrations.DeleteModel(
            name='Consulta',
        ),
        migrations.DeleteModel(
            name='Medicamento',
        ),
        migrations.DeleteModel(
            name='Tratamiento',
        ),
    ]