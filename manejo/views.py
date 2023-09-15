from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Animales, Vacunacion, Paricion
from django.shortcuts import render

def cargar_vacunacion(request):
  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())
  return render(request, 'carga_vacunas.html',{
    'animales':animales,
    'vacunacion': vacunacion,
    'paricion': paricion
  })

def paricion(request):
  paricion = list(Vacunacion.objects.values())

  return render(request, '')

def carga_animal(request):
  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())

  return render(request, 'carga_animales.html',{
    'animales':animales,
    'vacunacion': vacunacion,
    'paricion': paricion
  })

def lista_animales(request):
  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())
  return render(request, 'lista_animales.html',{
    'animales': animales,
    'vacunacion': vacunacion,
    'paricion': paricion
  })