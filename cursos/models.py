from django.db import models
from usuarios.models import Usuario


class Curso(models.Model):
    """10mo A, 10mo B, 1ro Bach A, etc."""
    NIVELES = (
        ('10mo', 'Décimo Año'),
        ('1ro_bach', 'Primero de Bachillerato'),
        ('2do_bach', 'Segundo de Bachillerato'),
        ('3ro_bach', 'Tercero de Bachillerato'),
    )
    nivel    = models.CharField(max_length=20, choices=NIVELES, default='10mo')
    paralelo = models.CharField(max_length=5)   # A, B, C, D
    descripcion = models.TextField(blank=True)

    @property
    def nombre(self):
        return f"{self.get_nivel_display()} «{self.paralelo}»"

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nivel', 'paralelo']
        unique_together = ('nivel', 'paralelo')


class Materia(models.Model):
    """Programación, Diseño, Matemáticas…  dentro de un Curso."""
    nombre  = models.CharField(max_length=120)
    curso   = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materias')
    profesor = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='materias', limit_choices_to={'rol': 'profesor'}
    )

    def __str__(self):
        return f"{self.nombre} — {self.curso}"

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['nombre']
        unique_together = ('nombre', 'curso')


class Estudiante(models.Model):
    nombre   = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula   = models.CharField(max_length=20, unique=True, blank=True, null=True)
    curso    = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estudiantes')

    def __str__(self):
        return f"{self.apellido} {self.nombre}"

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['apellido', 'nombre']
