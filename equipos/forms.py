import re
from django import forms
from django.utils.html import escape
from .models import PrestamoEquipo


def sanitize_input(texto: str) -> str:
    limpio = escape((texto or '').strip())
    return re.sub(r'\s+', ' ', limpio)


class PrestamoEquipoForm(forms.ModelForm):
    class Meta:
        model = PrestamoEquipo
        fields = ['equipo', 'cantidad', 'fecha_prestamo', 'fecha_devolucion', 'observaciones']
        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_observaciones(self):
        obs = self.cleaned_data.get('observaciones', '')
        return sanitize_input(obs)

    def clean(self):
        cleaned = super().clean()
        equipo = cleaned.get('equipo')
        cantidad = cleaned.get('cantidad') or 0
        f_prestamo = cleaned.get('fecha_prestamo')
        f_devolucion = cleaned.get('fecha_devolucion')

        if f_prestamo and f_devolucion and f_devolucion <= f_prestamo:
            self.add_error('fecha_devolucion', 'La fecha de devolución debe ser posterior a la fecha de préstamo.')

        if equipo:
            if equipo.estado != 'operativo':
                self.add_error('equipo', 'Solo se pueden prestar equipos en estado operativo.')
            if cantidad > equipo.stock_disponible:
                self.add_error('cantidad', f'Stock insuficiente (disponibles: {equipo.stock_disponible}).')

        if self.user and self.user.is_authenticated:
            activos = PrestamoEquipo.objects.filter(docente=self.user, estado='activo').count()
            if activos >= 3:
                raise forms.ValidationError('No puedes tener más de 3 préstamos activos simultáneamente.')

        return cleaned