from django.db import models
from datetime import date

class Parentesco(models.Model):
    id_parentesco = models.AutoField(primary_key=True)
    parentesco_nombre = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'parentescos'
        managed = False
        
    def __str__(self):
        return self.parentesco_nombre

class Tutor(models.Model):
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    dni_tutor = models.IntegerField(primary_key=True)
    nombre_tutor = models.CharField(max_length=35)
    apellido_tutor = models.CharField(max_length=35)
    telefono_tutor = models.CharField(max_length=15)
    correo_tutor = models.EmailField(max_length=100)
    genero_tutor = models.CharField(max_length=1, choices=GENERO_OPCIONES, null=True, blank=True)

    class Meta:
        db_table = 'tutores'
        managed = False
        ordering = ['apellido_tutor', 'nombre_tutor']

    def __str__(self):
        return f"{self.apellido_tutor}, {self.nombre_tutor} (DNI: {self.dni_tutor})"

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
        managed = False
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

    def obtener_tutores(self):
        """Método personalizado para obtener los tutores del alumno"""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t.*, p.parentesco_nombre 
                FROM alumno_x_tutor axt
                JOIN tutores t ON axt.dni_tutor = t.dni_tutor
                JOIN parentescos p ON axt.id_parentesco = p.id_parentesco
                WHERE axt.dni_alumno = %s
            """, [self.dni_alumno])
            return cursor.fetchall()

class AlumnoXTutor(models.Model):
    id_alumno_x_tutor = models.AutoField(primary_key=True)
    dni_tutor = models.IntegerField()  
    dni_alumno = models.IntegerField()  
    id_parentesco = models.IntegerField()  
    
    class Meta:
        db_table = 'alumno_x_tutor'
        managed = False
        
    def __str__(self):
        return f"Alumno: {self.dni_alumno} - Tutor: {self.dni_tutor} - Parentesco: {self.id_parentesco}"

    
    def get_tutor(self):
        try:
            return Tutor.objects.get(dni_tutor=self.dni_tutor)
        except Tutor.DoesNotExist:
            return None

    def get_alumno(self):
        try:
            return Alumno.objects.get(dni_alumno=self.dni_alumno)
        except Alumno.DoesNotExist:
            return None

    def get_parentesco(self):
        try:
            return Parentesco.objects.get(id_parentesco=self.id_parentesco)
        except Parentesco.DoesNotExist:
            return None

class Grado(models.Model):
    id_grado = models.AutoField(primary_key=True)
    nombre_grado = models.CharField(max_length=50)
    asientos_disponibles = models.IntegerField()
    
    class Meta:
        db_table = 'grados'
        managed = False
        ordering = ['nombre_grado']
        
    def __str__(self):
        return self.nombre_grado

class AlumnoXGrado(models.Model):
    id_alumno_x_grado = models.AutoField(primary_key=True)
    dni_alumno = models.IntegerField()  
    id_grado = models.IntegerField()  
    anio = models.IntegerField()
    
    class Meta:
        db_table = 'alumnos_x_grados'
        managed = False
        
    def __str__(self):
        return f"Alumno: {self.dni_alumno} - Grado: {self.id_grado} - Año: {self.anio}"

    
    def get_alumno(self):
        try:
            return Alumno.objects.get(dni_alumno=self.dni_alumno)
        except Alumno.DoesNotExist:
            return None

    def get_grado(self):
        try:
            return Grado.objects.get(id_grado=self.id_grado)
        except Grado.DoesNotExist:
            return None


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'roles'
        managed = False
        
    def __str__(self):
        return self.nombre_rol

class Empleado(models.Model):
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    dni_empleado = models.IntegerField(primary_key=True)
    nombre_empleado = models.CharField(max_length=35)
    apellido_empleado = models.CharField(max_length=35)
    telefono_empleado = models.CharField(max_length=15, null=False)
    genero_empleado = models.CharField(max_length=1, choices=GENERO_OPCIONES)
    id_rol = models.IntegerField()  
    
    class Meta:
        db_table = 'empleados'
        managed = False
        ordering = ['apellido_empleado', 'nombre_empleado']
        
    def __str__(self):
        return f"{self.apellido_empleado}, {self.nombre_empleado}"

    def get_rol(self):
        try:
            return Rol.objects.get(id_rol=self.id_rol)
        except Rol.DoesNotExist:
            return None

class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    nombre_asignatura = models.CharField(max_length=45)
    descripcion_asignatura = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'asignaturas'
        managed = False
        
    def __str__(self):
        return self.nombre_asignatura

class DictadoClase(models.Model):
    dictado_clase = models.AutoField(primary_key=True)
    id_grado = models.IntegerField()  
    id_asignatura = models.IntegerField()  
    dni_empleado = models.IntegerField()  
    
    class Meta:
        db_table = 'dictados_clases'
        managed = False
        
    def __str__(self):
        return f"Dictado: {self.dictado_clase} - Grado: {self.id_grado} - Asignatura: {self.id_asignatura}"

    
    def get_grado(self):
        try:
            return Grado.objects.get(id_grado=self.id_grado)
        except Grado.DoesNotExist:
            return None

    def get_asignatura(self):
        try:
            return Asignatura.objects.get(id_asignatura=self.id_asignatura)
        except Asignatura.DoesNotExist:
            return None

    def get_empleado(self):
        try:
            return Empleado.objects.get(dni_empleado=self.dni_empleado)
        except Empleado.DoesNotExist:
            return None