from django.urls import path
from . import views

urlpatterns = [
    path('Cargar_Vacunacion/', views.cargar_vacunacion, name="carga_vacunas"),
    path('Pariciones/', views.paricion, name="pariciones" ),
    path('Cargar_animales/', views.carga_animal, name="cargar_animales"),
    path('', views.lista_animales, name="lista_animales")
]