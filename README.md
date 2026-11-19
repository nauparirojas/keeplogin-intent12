# Práctica Grupal pero individual fallada de la Semana 12 (UNCP)

Sistema backend en Django desarrollado para la asignatura **Desarrollo de Aplicaciones Web (IS093A)**, implementando:
- **Caso 1:** Gestión de préstamos de equipos de laboratorio (validaciones `clean_observaciones()` y `clean()` sobre stock, estado operativo, fechas y límite de 3 préstamos activos; sanitización con `escape()`).
- **Caso 2:** Plataforma de gestión de consultas médicas (validación de DNI de 8 dígitos, fecha de nacimiento no futura, correo `@uncp.edu.pe`, horario de atención y citas duplicadas).
- **Seguridad, Middleware y Admin:** `AuditoriaSistemaMiddleware`, sesión con expiración por inactividad, CSRF en formularios POST y `ModelAdmin` personalizado con filtros, búsquedas, campos calculados y acciones masivas.

## Instalación y ejecución
1. Crear y activar entorno virtual: `python -m venv venv` y `.\venv\Scripts\Activate`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Aplicar migraciones y crear superusuario: `python manage.py migrate` y `python manage.py createsuperuser`
4. Levantar servidor: `python manage.py runserver`
