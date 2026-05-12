from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Usuario
from .forms import LoginForm, ProfesorForm
from cursos.models import Curso


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.es_admin():
        from cursos.models import Materia, Estudiante
        total_profesores  = Usuario.objects.filter(rol='profesor').count()
        total_cursos      = Curso.objects.count()
        total_materias    = Materia.objects.count()
        total_estudiantes = Estudiante.objects.count()
        cursos_recientes  = Curso.objects.prefetch_related('materias','estudiantes').order_by('nivel','paralelo')[:8]
        context = {
            'total_profesores':  total_profesores,
            'total_cursos':      total_cursos,
            'total_materias':    total_materias,
            'total_estudiantes': total_estudiantes,
            'cursos_recientes':  cursos_recientes,
        }
        return render(request, 'usuarios/dashboard_admin.html', context)
    else:
        from cursos.models import Materia
        materias = Materia.objects.filter(profesor=user).select_related('curso').order_by('curso__nivel','curso__paralelo','nombre')
        grupos = {}
        for m in materias:
            grupos.setdefault(m.curso, []).append(m)
        context = {
            'grupos': grupos,
            'total_materias': materias.count(),
            'total_cursos': len(grupos),
        }
        return render(request, 'usuarios/dashboard_profesor.html', context)


@login_required
def lista_profesores(request):
    if not request.user.es_admin():
        messages.error(request, 'No tienes permiso para ver esta página.')
        return redirect('dashboard')
    profesores = Usuario.objects.filter(rol='profesor').order_by('last_name', 'first_name')
    return render(request, 'usuarios/lista_profesores.html', {'profesores': profesores})


@login_required
def crear_profesor(request):
    if not request.user.es_admin():
        messages.error(request, 'No tienes permiso.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            profesor = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if not password:
                messages.error(request, 'La contraseña es obligatoria al crear un profesor.')
                return render(request, 'usuarios/form_profesor.html', {'form': form, 'accion': 'Crear'})
            profesor.set_password(password)
            profesor.rol = 'profesor'
            profesor.save()
            messages.success(request, f'Profesor {profesor.get_full_name() or profesor.username} creado exitosamente.')
            return redirect('lista_profesores')
    else:
        form = ProfesorForm()
    return render(request, 'usuarios/form_profesor.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_profesor(request, pk):
    if not request.user.es_admin():
        messages.error(request, 'No tienes permiso.')
        return redirect('dashboard')
    profesor = get_object_or_404(Usuario, pk=pk, rol='profesor')
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profesor actualizado correctamente.')
            return redirect('lista_profesores')
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, 'usuarios/form_profesor.html', {'form': form, 'accion': 'Editar', 'profesor': profesor})


@login_required
def eliminar_profesor(request, pk):
    if not request.user.es_admin():
        messages.error(request, 'No tienes permiso.')
        return redirect('dashboard')
    profesor = get_object_or_404(Usuario, pk=pk, rol='profesor')
    if request.method == 'POST':
        nombre = profesor.get_full_name() or profesor.username
        profesor.delete()
        messages.success(request, f'Profesor {nombre} eliminado.')
        return redirect('lista_profesores')
    return render(request, 'usuarios/confirmar_eliminar.html', {'objeto': profesor, 'tipo': 'profesor'})
