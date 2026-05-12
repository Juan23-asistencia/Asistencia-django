#!/usr/bin/env python
"""
Script de configuración inicial — EduAsistencia v3
Crea cursos (10mo A-D, 1ro Bach A-D, 2do Bach A-C, 3ro Bach A-C),
profesores de ejemplo y materias con asignaciones.
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_attendance.settings')
django.setup()

from usuarios.models import Usuario
from cursos.models import Curso, Materia, Estudiante

print("\n" + "="*55)
print("  EduAsistencia — Configuración Inicial v3")
print("="*55)

# ── 1. ADMINISTRADOR ──────────────────────────────────────
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser(
        username='admin', password='admin123',
        email='admin@escuela.edu',
        first_name='Administrador', last_name='Sistema', rol='admin'
    )
    print("\n✅ Admin: admin / admin123")
else:
    print("\n⚠️  Admin ya existe.")

# ── 2. PROFESORES ─────────────────────────────────────────
profs_data = [
    ('andy_calva',    'Andy',    'Calva',    'andy@escuela.edu'),
    ('prof_garcia',   'María',   'García',   'garcia@escuela.edu'),
    ('prof_lopez',    'Carlos',  'López',    'lopez@escuela.edu'),
    ('prof_torres',   'Rosa',    'Torres',   'torres@escuela.edu'),
    ('prof_mendoza',  'Luis',    'Mendoza',  'mendoza@escuela.edu'),
]
profs = {}
for uname, fn, ln, email in profs_data:
    if not Usuario.objects.filter(username=uname).exists():
        u = Usuario.objects.create_user(username=uname, password='prof123',
                                        first_name=fn, last_name=ln,
                                        email=email, rol='profesor')
        print(f"✅ Profesor: {uname} / prof123")
    else:
        u = Usuario.objects.get(username=uname)
        print(f"⚠️  Profesor '{uname}' ya existe.")
    profs[uname] = u

# ── 3. CURSOS ─────────────────────────────────────────────
estructura = [
    ('10mo',     ['A','B','C','D']),
    ('1ro_bach', ['A','B','C','D']),
    ('2do_bach', ['A','B','C']),
    ('3ro_bach', ['A','B','C']),
]
cursos = {}
for nivel, paralelos in estructura:
    for p in paralelos:
        c, created = Curso.objects.get_or_create(nivel=nivel, paralelo=p)
        cursos[f"{nivel}_{p}"] = c
        mark = "✅" if created else "⚠️ "
        print(f"{mark} Curso: {c}")

# ── 4. MATERIAS con profesores ────────────────────────────
# 3ro Bach A  →  Andy Calva: Programación, Diseño, Sistemas
c3a = cursos['3ro_bach_A']
for nombre, prof_key in [
    ('Programación',    'andy_calva'),
    ('Diseño',          'andy_calva'),
    ('Sistemas',        'andy_calva'),
    ('Matemáticas',     'prof_garcia'),
    ('Lengua',          'prof_lopez'),
]:
    m, cr = Materia.objects.get_or_create(nombre=nombre, curso=c3a,
                                          defaults={'profesor': profs[prof_key]})
    if not cr:
        m.profesor = profs[prof_key]; m.save()
    print(f"{'✅' if cr else '⚠️ '} Materia: {m.nombre} ({c3a}) → {profs[prof_key].get_full_name()}")

# 3ro Bach B y C
for k in ['3ro_bach_B','3ro_bach_C']:
    c = cursos[k]
    for nombre, pk in [('Programación','andy_calva'),('Diseño','andy_calva'),('Matemáticas','prof_garcia')]:
        m, cr = Materia.objects.get_or_create(nombre=nombre, curso=c,
                                              defaults={'profesor': profs[pk]})
        if not cr: m.profesor = profs[pk]; m.save()

# 2do Bach
for k in ['2do_bach_A','2do_bach_B','2do_bach_C']:
    c = cursos[k]
    for nombre, pk in [('Matemáticas','prof_garcia'),('Física','prof_mendoza'),('Lengua','prof_lopez'),('Inglés','prof_torres')]:
        m, cr = Materia.objects.get_or_create(nombre=nombre, curso=c,
                                              defaults={'profesor': profs[pk]})
        if not cr: m.profesor = profs[pk]; m.save()

# 10mo y 1ro Bach
for nivel in ['10mo','1ro_bach']:
    for p in (['A','B','C','D']):
        c = cursos[f'{nivel}_{p}']
        for nombre, pk in [('Matemáticas','prof_garcia'),('Lengua','prof_lopez'),('Inglés','prof_torres'),('Ciencias','prof_mendoza')]:
            m, cr = Materia.objects.get_or_create(nombre=nombre, curso=c,
                                                  defaults={'profesor': profs[pk]})
            if not cr: m.profesor = profs[pk]; m.save()

print("\n✅ Materias asignadas correctamente.")

# ── 5. ESTUDIANTES de ejemplo (solo 3ro A y 3ro B) ────────
ests = [
    ('Lucía','Andrade','0912345671','3ro_bach_A'),
    ('Sebastián','Benítez','0923456782','3ro_bach_A'),
    ('Valeria','Castro','0934567893','3ro_bach_A'),
    ('Mateo','Díaz','0945678904','3ro_bach_A'),
    ('Daniela','Espinosa','0956789015','3ro_bach_A'),
    ('Camila','Flores','0967890126','3ro_bach_B'),
    ('Andrés','Gómez','0978901237','3ro_bach_B'),
    ('Isabella','Herrera','0989012348','3ro_bach_B'),
]
for fn, ln, ced, ck in ests:
    if not Estudiante.objects.filter(cedula=ced).exists():
        Estudiante.objects.create(nombre=fn, apellido=ln, cedula=ced, curso=cursos[ck])
        print(f"✅ Estudiante: {ln} {fn} → {cursos[ck]}")

print("\n" + "="*55)
print("  ¡Listo!")
print("="*55)
print("\nCredenciales:")
print("  Admin    → admin / admin123")
print("  Profesor → andy_calva / prof123  (Programación, Diseño, Sistemas en 3ro)")
print("  Profesor → prof_garcia / prof123  (Matemáticas)")
print("  Profesor → prof_lopez  / prof123  (Lengua)")
print("\nEjecuta: python manage.py runserver")
print("Abre: http://127.0.0.1:8000\n")
