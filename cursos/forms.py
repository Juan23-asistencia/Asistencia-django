from django import forms
from .models import Curso, Materia, Estudiante
from usuarios.models import Usuario


class CursoForm(forms.ModelForm):
    class Meta:
        model  = Curso
        fields = ['nivel', 'paralelo', 'descripcion']
        labels = {
            'nivel':       'Nivel / Año',
            'paralelo':    'Paralelo',
            'descripcion': 'Descripción (opcional)',
        }
        widgets = {
            'nivel':       forms.Select(attrs={'class': 'form-select'}),
            'paralelo':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A, B, C, D'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model  = Materia
        fields = ['nombre', 'profesor']
        labels = {'nombre': 'Nombre de la materia', 'profesor': 'Profesor asignado'}
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Programación'}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Usuario.objects.filter(rol='profesor').order_by('last_name')
        self.fields['profesor'].empty_label = '— Sin asignar —'


class EstudianteForm(forms.ModelForm):
    class Meta:
        model  = Estudiante
        fields = ['nombre', 'apellido', 'cedula']
        labels = {'nombre': 'Nombre', 'apellido': 'Apellido', 'cedula': 'Cédula / ID'}
        widgets = {
            'nombre':   forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula':   forms.TextInput(attrs={'class': 'form-control'}),
        }
