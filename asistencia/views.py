import datetime, calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asistencia
from cursos.models import Curso, Materia, Estudiante
from usuarios.models import Usuario


@login_required
def tomar_asistencia(request, materia_pk):
    user    = request.user
    materia = get_object_or_404(Materia, pk=materia_pk)

    if not user.es_admin() and materia.profesor != user:
        messages.error(request, 'No tienes acceso a esta materia.')
        return redirect('lista_cursos')

    hoy         = datetime.date.today()
    estudiantes = materia.curso.estudiantes.all()

    asistencias_hoy = {
        a.estudiante_id: a
        for a in Asistencia.objects.filter(materia=materia, fecha=hoy)
    }

    if request.method == 'POST':
        fecha_str = request.POST.get('fecha', str(hoy))
        try:
            fecha = datetime.date.fromisoformat(fecha_str)
        except ValueError:
            fecha = hoy

        for est in estudiantes:
            estado = request.POST.get(f'estado_{est.pk}', 'ausente')
            Asistencia.objects.update_or_create(
                estudiante=est, materia=materia, fecha=fecha,
                defaults={'profesor': user, 'estado': estado}
            )
        messages.success(request, f'Asistencia del {fecha.strftime("%d/%m/%Y")} guardada.')
        return redirect('detalle_materia', pk=materia_pk)

    return render(request, 'asistencia/tomar_asistencia.html', {
        'materia':        materia,
        'curso':          materia.curso,
        'estudiantes':    estudiantes,
        'hoy':            hoy,
        'asistencias_hoy': asistencias_hoy,
    })


@login_required
def reporte_asistencia(request):
    if not request.user.es_admin():
        messages.error(request, 'Sin permiso.'); return redirect('dashboard')

    hoy  = datetime.date.today()
    mes  = int(request.GET.get('mes',  hoy.month))
    anio = int(request.GET.get('anio', hoy.year))

    curso_id   = request.GET.get('curso')
    materia_id = request.GET.get('materia')

    cursos             = Curso.objects.prefetch_related('materias').all()
    curso_seleccionado   = None
    materia_seleccionada = None
    materias_del_curso   = []
    reporte              = []

    if curso_id:
        curso_seleccionado = get_object_or_404(Curso, pk=curso_id)
        materias_del_curso = curso_seleccionado.materias.select_related('profesor').all()

    if materia_id:
        materia_seleccionada = get_object_or_404(Materia, pk=materia_id)
        for est in materia_seleccionada.curso.estudiantes.all():
            qs        = Asistencia.objects.filter(estudiante=est, materia=materia_seleccionada,
                                                   fecha__month=mes, fecha__year=anio)
            presentes = qs.filter(estado='presente').count()
            ausentes  = qs.filter(estado='ausente').count()
            total     = presentes + ausentes
            reporte.append({
                'estudiante': est,
                'presentes':  presentes,
                'ausentes':   ausentes,
                'total':      total,
                'porcentaje': round(presentes / total * 100, 1) if total else 0,
            })

    MESES = [(1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),
             (7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre')]

    return render(request, 'asistencia/reporte.html', {
        'cursos':               cursos,
        'curso_seleccionado':   curso_seleccionado,
        'materias_del_curso':   materias_del_curso,
        'materia_seleccionada': materia_seleccionada,
        'reporte':              reporte,
        'mes': mes, 'anio': anio,
        'meses': MESES,
        'anios': list(range(hoy.year - 2, hoy.year + 1)),
        'nombre_mes': dict(MESES).get(mes, ''),
    })


@login_required
def calendario_estudiante(request, estudiante_pk):
    if not request.user.es_admin():
        messages.error(request, 'Sin permiso.'); return redirect('dashboard')

    estudiante  = get_object_or_404(Estudiante, pk=estudiante_pk)
    hoy         = datetime.date.today()
    mes         = int(request.GET.get('mes',  hoy.month))
    anio        = int(request.GET.get('anio', hoy.year))
    materia_id  = request.GET.get('materia')

    materias_del_curso = estudiante.curso.materias.select_related('profesor').all()
    materia_sel = None
    if materia_id:
        materia_sel = get_object_or_404(Materia, pk=materia_id, curso=estudiante.curso)

    # filtro por materia si fue seleccionada
    qs_base = Asistencia.objects.filter(estudiante=estudiante, fecha__month=mes, fecha__year=anio)
    if materia_sel:
        qs_base = qs_base.filter(materia=materia_sel)

    asistencias_dict = {a.fecha.day: a.estado for a in qs_base}

    cal_data = calendar.monthcalendar(anio, mes)
    semanas  = []
    for semana in cal_data:
        dias = []
        for dia in semana:
            if dia == 0:
                dias.append({'dia': None, 'estado': None})
            else:
                dias.append({'dia': dia, 'estado': asistencias_dict.get(dia)})
        semanas.append(dias)

    presentes  = qs_base.filter(estado='presente').count()
    ausentes   = qs_base.filter(estado='ausente').count()
    total      = presentes + ausentes

    MESES_N = ['','Enero','Febrero','Marzo','Abril','Mayo','Junio',
               'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

    mes_ant  = 12 if mes == 1  else mes - 1
    anio_ant = anio - 1 if mes == 1  else anio
    mes_sig  = 1  if mes == 12 else mes + 1
    anio_sig = anio + 1 if mes == 12 else anio

    return render(request, 'asistencia/calendario.html', {
        'estudiante':        estudiante,
        'materias_del_curso': materias_del_curso,
        'materia_sel':       materia_sel,
        'semanas':           semanas,
        'mes': mes, 'anio': anio,
        'nombre_mes':        MESES_N[mes],
        'mes_anterior':      mes_ant, 'anio_anterior': anio_ant,
        'mes_siguiente':     mes_sig, 'anio_siguiente': anio_sig,
        'presentes':         presentes,
        'ausentes':          ausentes,
        'total':             total,
        'porcentaje':        round(presentes / total * 100, 1) if total else 0,
        'hoy':               hoy,
    })


@login_required
def historial_asistencia(request, materia_pk):
    user    = request.user
    materia = get_object_or_404(Materia, pk=materia_pk)

    if not user.es_admin() and materia.profesor != user:
        messages.error(request, 'Sin permiso.'); return redirect('lista_cursos')

    hoy  = datetime.date.today()
    mes  = int(request.GET.get('mes',  hoy.month))
    anio = int(request.GET.get('anio', hoy.year))

    asistencias = Asistencia.objects.filter(
        materia=materia, fecha__month=mes, fecha__year=anio
    ).select_related('estudiante', 'profesor').order_by('-fecha', 'estudiante__apellido')

    MESES = [(1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),
             (7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre')]

    return render(request, 'asistencia/historial.html', {
        'materia':    materia,
        'asistencias': asistencias,
        'mes': mes, 'anio': anio,
        'meses':      MESES,
        'anios':      list(range(hoy.year - 2, hoy.year + 1)),
        'nombre_mes': dict(MESES).get(mes, ''),
    })
