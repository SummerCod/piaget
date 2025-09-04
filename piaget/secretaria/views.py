from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Alumno
from .forms import AlumnoForm

class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumnos/alumno_list.html'
    context_object_name = 'alumnos'
    paginate_by = 10

class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/alumno_form.html'
    success_url = reverse_lazy('alumno_list')

class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/alumno_form.html'
    success_url = reverse_lazy('alumno_list')

class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumnos/alumno_confirm_delete.html'
    success_url = reverse_lazy('alumno_list')

def alumno_detail(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    return render(request, 'alumnos/alumno_detail.html', {'alumno': alumno})