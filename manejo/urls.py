from django.urls import path
from . import views

urlpatterns = [
    path('Cargar_Vacunacion/', views.cargar_vacunacion, name="carga_vacunas"),
    path('Cargar_pariciones/', views.paricion, name="carga_pariciones" ),
    path('Cargar_animales/', views.carga_animal, name="cargar_animales"),
    path('Editar/',views.editar, name="editar"),
    path('Lista_animales/', views.eliminar, name="eliminar"),
    path('', views.lista_animales, name="lista_animales")
]