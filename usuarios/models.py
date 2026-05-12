from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('profesor', 'Profesor'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='profesor')

    def es_admin(self):
        return self.rol == 'admin'

    def es_profesor(self):
        return self.rol == 'profesor'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"
