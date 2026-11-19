from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Equipo(models.Model):
    ESTADOS = [
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En mantenimiento'),
        ('baja', 'Dado de baja'),
    ]
    codigo_patrimonial = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    categoria = models.CharField(max_length=60)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='operativo')
    laboratorio = models.CharField(max_length=50)
    stock_disponible = models.PositiveIntegerField(default=1)
    ultimo_mantenimiento = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.codigo_patrimonial} - {self.nombre}"


class PrestamoEquipo(models.Model):
    ESTADOS_PRESTAMO = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ]
    docente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='prestamos')
    cantidad = models.PositiveIntegerField(default=1)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField()
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_PRESTAMO, default='activo')

    def __str__(self):
        return f"{self.docente.username} -> {self.equipo.codigo_patrimonial}"


class RegistroAuditoria(models.Model):
    usuario = models.CharField(max_length=150)
    ruta = models.CharField(max_length=255)
    metodo = models.CharField(max_length=10)
    ip = models.GenericIPAddressField(null=True, blank=True)
    detalle = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.creado_en:%Y-%m-%d %H:%M}] {self.usuario} - {self.detalle}"