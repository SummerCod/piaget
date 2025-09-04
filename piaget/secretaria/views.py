from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Alumno, AlumnoXTutor, Tutor, Parentesco
from .forms import AlumnoForm

class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumnos/alumno_list.html'
    context_object_name = 'alumnos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        
        dni = self.request.GET.get('dni')
        nombre = self.request.GET.get('nombre')
        apellido = self.request.GET.get('apellido')
        
        
        if dni:
            queryset = queryset.filter(dni_alumno__icontains=dni)
        if nombre:
            queryset = queryset.filter(nombre_alumno__icontains=nombre)
        if apellido:
            queryset = queryset.filter(apellido_alumno__icontains=apellido)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['is_filtered'] = any([
            self.request.GET.get('dni'),
            self.request.GET.get('nombre'),
            self.request.GET.get('apellido')
        ])
        
        query_string = ''
        for key, value in self.request.GET.items():
            if key != 'page' and value:
                query_string += f'{key}={value}&'
        context['query_string'] = query_string.rstrip('&')
        
        return context

class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/alumno_form.html'
    success_url = reverse_lazy('alumno_list')

    def form_valid(self, form):
        
        self.object = form.save()
        
        
        tutor_existente = form.cleaned_data.get('tutor_existente')
        parentesco = form.cleaned_data.get('parentesco')
        
        
        if tutor_existente and parentesco:
            
            AlumnoXTutor.objects.create(
                dni_tutor=tutor_existente.dni_tutor,  
                dni_alumno=self.object.dni_alumno,    
                id_parentesco=parentesco.id_parentesco  
            )
            messages.success(self.request, f'Alumno registrado exitosamente y vinculado al tutor {tutor_existente}')
        else:
            messages.success(self.request, 'Alumno registrado exitosamente')
        
        return redirect(self.get_success_url())
    
class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/alumno_form.html'
    success_url = reverse_lazy('alumno_list')

    def get_initial(self):
        initial = super().get_initial()
        
        relacion_tutor = AlumnoXTutor.objects.filter(dni_alumno=self.object.dni_alumno).first()
        if relacion_tutor:
            
            initial['tutor_existente'] = Tutor.objects.get(dni_tutor=relacion_tutor.dni_tutor)
            initial['parentesco'] = Parentesco.objects.get(id_parentesco=relacion_tutor.id_parentesco)
        return initial

    def form_valid(self, form):
        
        self.object = form.save()
        
        tutor_existente = form.cleaned_data.get('tutor_existente')
        parentesco = form.cleaned_data.get('parentesco')
        
        relacion_actual = AlumnoXTutor.objects.filter(dni_alumno=self.object.dni_alumno).first()
        
        if tutor_existente and parentesco:
            if relacion_actual:
                relacion_actual.dni_tutor = tutor_existente.dni_tutor  
                relacion_actual.id_parentesco = parentesco.id_parentesco  
                relacion_actual.save()
            else:
                
                AlumnoXTutor.objects.create(
                    dni_tutor=tutor_existente.dni_tutor,  
                    dni_alumno=self.object.dni_alumno,    
                    id_parentesco=parentesco.id_parentesco  
                )
            messages.success(self.request, f'Alumno actualizado y relación con tutor actualizada')
        elif relacion_actual:
            relacion_actual.delete()
            messages.success(self.request, 'Alumno actualizado y relación con tutor eliminada')
        else:
            messages.success(self.request, 'Alumno actualizado exitosamente')
        
        return redirect(self.get_success_url())


class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumnos/alumno_confirm_delete.html'
    success_url = reverse_lazy('alumno_list')

    def delete(self, request, *args, **kwargs):
        alumno = self.get_object()
        AlumnoXTutor.objects.filter(dni_alumno=alumno.dni_alumno).delete()
        messages.success(request, 'Alumno eliminado exitosamente')
        return super().delete(request, *args, **kwargs)


def crear_relacion_alumno_tutor(dni_alumno, dni_tutor, id_parentesco):
    relacion = AlumnoXTutor.objects.create(
        dni_alumno=dni_alumno,
        dni_tutor=dni_tutor,
        id_parentesco=id_parentesco
    )
    return relacion

def alumno_detail(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    
    relaciones_tutores = AlumnoXTutor.objects.filter(dni_alumno=alumno.dni_alumno)
    
    tutores_completos = []
    problemas = []
    
    for i, relacion in enumerate(relaciones_tutores):
        try:
            tutor = Tutor.objects.get(dni_tutor=relacion.dni_tutor)
            print(f"   ✅ Tutor encontrado: {tutor}")
        except Tutor.DoesNotExist:
            print(f"   ❌ Tutor con DNI {relacion.dni_tutor} NO EXISTE")
            problemas.append(f"Tutor con DNI {relacion.dni_tutor} no existe")
            continue
        
        try:
            parentesco = Parentesco.objects.get(id_parentesco=relacion.id_parentesco)
            print(f"   ✅ Parentesco encontrado: {parentesco}")
        except Parentesco.DoesNotExist:
            print(f"   ❌ Parentesco con ID {relacion.id_parentesco} NO EXISTE")
            problemas.append(f"Parentesco con ID {relacion.id_parentesco} no existe")
            continue
        
        tutores_completos.append({
            'tutor': tutor,
            'parentesco': parentesco,
            'relacion': relacion
        })
    
    context = {
        'alumno': alumno,
        'tutores_completos': tutores_completos,
        'problemas': problemas,  
    }
    return render(request, 'alumnos/alumno_detail.html', context)