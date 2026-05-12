from django.urls import path
from . import views

urlpatterns = [
    path('materias/<int:materia_pk>/asistencia/',  views.tomar_asistencia,     name='tomar_asistencia'),
    path('materias/<int:materia_pk>/historial/',   views.historial_asistencia, name='historial_asistencia'),
    path('reportes/',                              views.reporte_asistencia,   name='reporte_asistencia'),
    path('estudiantes/<int:estudiante_pk>/calendario/', views.calendario_estudiante, name='calendario_estudiante'),
]
