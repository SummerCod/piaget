from django.db import models
from datetime import date

class Alumno(models.Model):
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    dni_alumno = models.IntegerField(primary_key=True)
    nombre_alumno = models.CharField(max_length=35)
    apellido_alumno = models.CharField(max_length=35)
    fecha_nacimiento_alumno = models.DateField(null=True, blank=True)
    genero_alumno = models.CharField(max_length=1, choices=GENERO_OPCIONES, null=True, blank=True)

    class Meta:
        db_table = 'alumnos'
        ordering = ['apellido_alumno', 'nombre_alumno']

    def __str__(self):
        return f"{self.apellido_alumno}, {self.nombre_alumno} (DNI: {self.dni_alumno})"

    def get_edad(self):
        if self.fecha_nacimiento_alumno:
            today = date.today()
            return today.year - self.fecha_nacimiento_alumno.year - (
                (today.month, today.day) < (self.fecha_nacimiento_alumno.month, self.fecha_nacimiento_alumno.day)
            )
        return None

