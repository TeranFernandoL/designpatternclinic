from django.contrib import admin

from .models import *


class TratamientoInline(admin.StackedInline):
    model = Tratamiento
    extra = 1
    max_num = 1


class EspecialidadInline(admin.StackedInline):
    model = Especialidad
    extra = 2


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    pass


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    pass


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    search_fields = ('paciente', 'medico')
    list_filter = ('fecha',)


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'presentacion', 'volumen', 'descripcion')


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha')
    search_fields = ('paciente', 'medico', 'fecha', 'diagnostico')
    inlines = [
        TratamientoInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()


@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    search_fields = ('consulta', 'medicamento', 'descripcion')
    filter_horizontal = ('medicamento',)


@admin.register(Consultorio)
class CosultorioAdmin(admin.ModelAdmin):
    pass
