import logging
from django.utils import timezone
from .models import PrestamoEquipo, RegistroAuditoria

logger = logging.getLogger('auditoria')


class AuditoriaSistemaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _obtener_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def __call__(self, request):
        usuario = request.user.username if request.user.is_authenticated else 'anonimo'
        ip = self._obtener_ip(request)

        if request.user.is_authenticated and not request.session.get('aviso_vencidos_mostrado'):
            vencidos = PrestamoEquipo.objects.filter(
                docente=request.user,
                estado='activo',
                fecha_devolucion__lt=timezone.now().date()
            ).count()
            if vencidos > 0:
                request.session['alerta_prestamos_vencidos'] = f'Tienes {vencidos} préstamo(s) vencido(s) por devolver.'
            request.session['aviso_vencidos_mostrado'] = True

        response = self.get_response(request)

        if request.method in ('POST', 'PUT', 'DELETE') or response.status_code in (401, 403):
            detalle = f"Acceso denegado ({response.status_code})" if response.status_code in (401, 403) else f"Acción {request.method}"
            logger.warning(f"AUDITORIA | user={usuario} | ip={ip} | path={request.path} | {detalle}")
            try:
                RegistroAuditoria.objects.create(
                    usuario=usuario,
                    ruta=request.path[:255],
                    metodo=request.method,
                    ip=ip,
                    detalle=detalle
                )
            except Exception:
                pass

        return response