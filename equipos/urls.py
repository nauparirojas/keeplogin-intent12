from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('prestamos/nuevo/', views.solicitar_prestamo_view, name='prestamo_nuevo'),
]