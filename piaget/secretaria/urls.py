from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/', views.AlumnoListView.as_view(), name='alumno_list'),
    path('alumnos/nuevo/', views.AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumnos/<int:pk>/eliminar/', views.AlumnoDeleteView.as_view(), name='alumno_delete'),
    path('alumnos/<int:pk>/', views.alumno_detail, name='alumno_detail'),
]