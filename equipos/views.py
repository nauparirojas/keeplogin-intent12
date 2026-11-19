from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Equipo, PrestamoEquipo
from .forms import PrestamoEquipoForm


@login_required
def inicio_view(request):
    alerta_vencidos = request.session.pop('alerta_prestamos_vencidos', None)
    equipos = Equipo.objects.all()
    if request.user.is_staff:
        prestamos = PrestamoEquipo.objects.select_related('docente', 'equipo').all()
    else:
        prestamos = PrestamoEquipo.objects.select_related('docente', 'equipo').filter(docente=request.user)
    return render(request, 'equipos/inicio.html', {
        'equipos': equipos,
        'prestamos': prestamos,
        'alerta_vencidos': alerta_vencidos,
    })


@login_required
def solicitar_prestamo_view(request):
    if request.method == 'POST':
        form = PrestamoEquipoForm(request.POST, user=request.user)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.docente = request.user
            prestamo.save()
            equipo = prestamo.equipo
            equipo.stock_disponible = max(0, equipo.stock_disponible - prestamo.cantidad)
            equipo.save(update_fields=['stock_disponible'])
            messages.success(request, 'Préstamo registrado correctamente.')
            return redirect('inicio')
    else:
        form = PrestamoEquipoForm(user=request.user)
    return render(request, 'equipos/prestamo_form.html', {'form': form})