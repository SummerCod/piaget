from django import forms
from .models import Alumno, Tutor, Parentesco

class AlumnoForm(forms.ModelForm):
    tutor_existente = forms.ModelChoiceField(
        queryset=Tutor.objects.all().order_by('apellido_tutor', 'nombre_tutor'),
        required=False,
        label="Seleccionar Tutor Existente",
        empty_label="-- Seleccionar tutor existente --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parentesco = forms.ModelChoiceField(
        queryset=Parentesco.objects.all(),
        required=True,
        label="Parentesco",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'fecha_nacimiento_alumno': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dni_alumno': forms.NumberInput(attrs={
                'min': 1000000, 
                'max': 99999999,
                'class': 'form-control'
            }),
            'nombre_alumno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_alumno': forms.TextInput(attrs={'class': 'form-control'}),
            'genero_alumno': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'dni_alumno': 'DNI',
            'nombre_alumno': 'Nombre',
            'apellido_alumno': 'Apellido',
            'fecha_nacimiento_alumno': 'Fecha de Nacimiento',
            'genero_alumno': 'Género',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
        if self.instance and self.instance.pk:
            self.fields['dni_alumno'].widget.attrs['readonly'] = True
            self.fields['dni_alumno'].help_text = "El DNI no puede ser modificado una vez creado el alumno"

    def clean_dni_alumno(self):
        dni = self.cleaned_data.get('dni_alumno')
        if dni < 1000000 or dni > 99999999:
            raise forms.ValidationError("El DNI debe tener entre 7 y 8 dígitos")
    
    
        if self.instance and self.instance.pk:
            if Alumno.objects.filter(dni_alumno=dni).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este DNI ya está registrado por otro alumno")
        else:
            if Alumno.objects.filter(dni_alumno=dni).exists():
                raise forms.ValidationError("Este DNI ya está registrado")
    
        return dni

    def clean(self):
        cleaned_data = super().clean()
        tutor_existente = cleaned_data.get('tutor_existente')
        parentesco = cleaned_data.get('parentesco')

        if tutor_existente and not parentesco:
            self.add_error('parentesco', "Debe seleccionar un parentesco cuando elige un tutor existente")
        
        if parentesco and not tutor_existente:
            self.add_error('tutor_existente', "Debe seleccionar un tutor cuando elige un parentesco")

        return cleaned_data