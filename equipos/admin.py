from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Equipo, PrestamoEquipo, RegistroAuditoria


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_patrimonial', 'nombre', 'categoria', 'laboratorio',
        'stock_disponible', 'estado_color', 'dias_desde_mantenimiento'
    )
    list_filter = ('laboratorio', 'estado', 'categoria')
    search_fields = ('codigo_patrimonial', 'nombre', 'categoria')
    actions = ['marcar_mantenimiento']

    @admin.display(description='Estado')
    def estado_color(self, obj):
        colores = {'operativo': '#198754', 'mantenimiento': '#d97706', 'baja': '#dc3545'}
        color = colores.get(obj.estado, '#333')
        return format_html('<strong style="color:{};">{}</strong>', color, obj.get_estado_display())

    @admin.display(description='Días sin mantenimiento')
    def dias_desde_mantenimiento(self, obj):
        return (timezone.now().date() - obj.ultimo_mantenimiento).days

    @admin.action(description='Marcar como en mantenimiento')
    def marcar_mantenimiento(self, request, queryset):
        queryset.update(estado='mantenimiento')


@admin.register(PrestamoEquipo)
class PrestamoEquipoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'equipo', 'cantidad', 'fecha_prestamo', 'fecha_devolucion', 'estado', 'dias_retraso')
    list_filter = ('estado', 'fecha_prestamo', 'docente')
    search_fields = ('equipo__codigo_patrimonial', 'docente__username', 'docente__first_name')
    list_select_related = ('docente', 'equipo')
    actions = ['enviar_recordatorio_devolucion']

    @admin.display(description='Días de retraso')
    def dias_retraso(self, obj):
        hoy = timezone.now().date()
        if obj.estado == 'activo' and hoy > obj.fecha_devolucion:
            return (hoy - obj.fecha_devolucion).days
        return 0

    @admin.action(description='Enviar recordatorio de devolución')
    def enviar_recordatorio_devolucion(self, request, queryset):
        self.message_user(request, f"Recordatorios generados para {queryset.count()} préstamo(s).")


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('creado_en', 'usuario', 'metodo', 'ruta', 'ip', 'detalle')
    list_filter = ('metodo', 'creado_en')
    search_fields = ('usuario', 'ruta', 'detalle')
    readonly_fields = ('usuario', 'ruta', 'metodo', 'ip', 'detalle', 'creado_en')