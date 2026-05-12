from django.contrib import admin
from .models import Curso, Materia, Estudiante

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nivel', 'paralelo']
    list_filter  = ['nivel']

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'curso', 'profesor']
    list_filter   = ['curso__nivel']
    search_fields = ['nombre']

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display  = ['apellido', 'nombre', 'cedula', 'curso']
    list_filter   = ['curso']
    search_fields = ['apellido', 'nombre', 'cedula']
