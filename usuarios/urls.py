from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profesores/', views.lista_profesores, name='lista_profesores'),
    path('profesores/crear/', views.crear_profesor, name='crear_profesor'),
    path('profesores/<int:pk>/editar/', views.editar_profesor, name='editar_profesor'),
    path('profesores/<int:pk>/eliminar/', views.eliminar_profesor, name='eliminar_profesor'),
]
