from django.db import models
from cursos.models import Curso, Materia, Estudiante
from usuarios.models import Usuario
import datetime


class Asistencia(models.Model):
    ESTADO_CHOICES = (
        ('presente', 'Presente'),
        ('ausente',  'Ausente'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')
    materia    = models.ForeignKey(Materia,    on_delete=models.CASCADE, related_name='asistencias')
    profesor   = models.ForeignKey(Usuario,    on_delete=models.SET_NULL, null=True, related_name='asistencias_registradas')
    fecha      = models.DateField(default=datetime.date.today)
    estado     = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='presente')

    class Meta:
        unique_together = ('estudiante', 'materia', 'fecha')
        ordering = ['-fecha']
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f"{self.estudiante} | {self.materia.nombre} | {self.fecha} | {self.estado}"
