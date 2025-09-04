from django.test import TestCase
from django.urls import reverse
from .models import Alumno

class AlumnoTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(
            dni_alumno=12345678,
            nombre_alumno="Juan",
            apellido_alumno="Pérez",
            fecha_nacimiento_alumno="2010-05-15",
            genero_alumno="M"
        )

    def test_alumno_creation(self):
        self.assertEqual(self.alumno.nombre_alumno, "Juan")
        self.assertEqual(self.alumno.apellido_alumno, "Pérez")

    def test_alumno_list_view(self):
        response = self.client.get(reverse('alumno_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juan")
        self.assertTemplateUsed(response, 'alumnos/alumno_list.html')

    def test_alumno_create_view(self):
        response = self.client.post(reverse('alumno_create'), {
            'dni_alumno': 87654321,
            'nombre_alumno': 'María',
            'apellido_alumno': 'Gómez',
            'fecha_nacimiento_alumno': '2011-08-20',
            'genero_alumno': 'F'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Alumno.objects.filter(dni_alumno=87654321).exists())