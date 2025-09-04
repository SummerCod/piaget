from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('dni_alumno', 'apellido_alumno', 'nombre_alumno', 'fecha_nacimiento_alumno', 'genero_alumno')
    list_filter = ('genero_alumno',)
    search_fields = ('dni_alumno', 'nombre_alumno', 'apellido_alumno')
    ordering = ('apellido_alumno', 'nombre_alumno')