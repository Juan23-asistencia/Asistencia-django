from django.urls import path
from . import views

urlpatterns = [
    # Cursos
    path('cursos/',                              views.lista_cursos,        name='lista_cursos'),
    path('cursos/<int:pk>/',                     views.detalle_curso,       name='detalle_curso'),
    path('cursos/crear/',                        views.crear_curso,         name='crear_curso'),
    path('cursos/<int:pk>/editar/',              views.editar_curso,        name='editar_curso'),
    path('cursos/<int:pk>/eliminar/',            views.eliminar_curso,      name='eliminar_curso'),
    # Materias
    path('cursos/<int:curso_pk>/materias/crear/', views.crear_materia,      name='crear_materia'),
    path('materias/<int:pk>/',                   views.detalle_materia,     name='detalle_materia'),
    path('materias/<int:pk>/editar/',            views.editar_materia,      name='editar_materia'),
    path('materias/<int:pk>/eliminar/',          views.eliminar_materia,    name='eliminar_materia'),
    # Estudiantes
    path('cursos/<int:curso_pk>/estudiantes/agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('cursos/<int:curso_pk>/estudiantes/agregar-ajax/', views.agregar_estudiante_ajax, name='agregar_estudiante_ajax'),
    path('cursos/<int:curso_pk>/estudiantes/importar/', views.importar_estudiantes, name='importar_estudiantes'),
    path('estudiantes/plantilla-excel/', views.descargar_plantilla_excel, name='descargar_plantilla_excel'),
    path('estudiantes/<int:pk>/editar/',         views.editar_estudiante,   name='editar_estudiante'),
    path('estudiantes/<int:pk>/eliminar/',       views.eliminar_estudiante, name='eliminar_estudiante'),
]
