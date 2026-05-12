from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('', include('usuarios.urls')),
    path('', include('cursos.urls')),
    path('', include('asistencia.urls')),
]
