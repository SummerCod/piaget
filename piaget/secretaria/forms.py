from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'fecha_nacimiento_alumno': forms.DateInput(attrs={'type': 'date'}),
            'dni_alumno': forms.NumberInput(attrs={'min': 1000000, 'max': 99999999}),
        }
        labels = {
            'dni_alumno': 'DNI',
            'nombre_alumno': 'Nombre',
            'apellido_alumno': 'Apellido',
            'fecha_nacimiento_alumno': 'Fecha de Nacimiento',
            'genero_alumno': 'Género',
        }

    def clean_dni_alumno(self):
        dni = self.cleaned_data.get('dni_alumno')
        if dni < 1000000 or dni > 99999999:
            raise forms.ValidationError("El DNI debe tener entre 7 y 8 dígitos")
        return dni