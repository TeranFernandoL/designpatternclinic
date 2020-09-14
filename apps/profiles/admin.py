from django.contrib import admin

from .models import *


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    pass


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    pass


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    search_fields = ('paciente', 'medico')
    list_filter = ('fecha',)

