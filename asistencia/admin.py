from django.contrib import admin
from .models import Asistencia

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display  = ['estudiante', 'materia', 'fecha', 'estado', 'profesor']
    list_filter   = ['estado', 'fecha', 'materia__curso']
    search_fields = ['estudiante__apellido', 'estudiante__nombre']
    date_hierarchy = 'fecha'
