import math
import os

import numpy as np
from .models import Animales, Vacunacion, Paricion, Vendido, Muerto
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, Q
from datetime import date, datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

# Def que nos permite cargar una vacunacion a la base de datos
def cargar_vacunacion(request):
  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())

  if request.method == 'GET':
    return render(request, 'carga_vacunas.html',{
      'animales':animales,
      'vacunacion': vacunacion,
      'paricion': paricion
    })
  else:
    if not(request.POST['caravana'] == 'Número de caravana'):
      id = Animales.objects.filter(nro_caravana = request.POST['caravana']).values('id').first()
      if not request.POST['fecha'] == '' and not request.POST['t_area'] == '':
        Vacunacion.objects.create(date=request.POST['fecha'], id_animal_id=id['id'],description=request.POST['t_area'])
      if not request.POST['fecha'] == '' and request.POST['t_area'] == '':
        Vacunacion.objects.create(date=request.POST['fecha'], id_animal_id=id['id'],description=request.POST['t_area'])
    
    return redirect('/')

# Def que nos permite cargar una paricion a la base de datos
def paricion(request):
  paricion = list(Paricion.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  animales = list(Animales.objects.values())

  if request.method == 'GET':
    return render(request, 'carga_paricion.html',{
      'animales':animales,
      'vacunacion': vacunacion,
      'paricion': paricion
    })
  else:
    if not(request.POST['caravana'] == 'Número de caravana'):
      id = Animales.objects.filter(nro_caravana = request.POST['caravana']).values('id').first()
      num = Animales.objects.get(id=id['id']).cant_pariciones
      animal = Animales.objects.get(id=id['id'])
      animal.cant_pariciones = num+1
      animal.save()
      if not(request.POST['fecha'] == ''):
        Paricion.objects.create(date=request.POST['fecha'], id_animal_id=id['id'])
        return redirect('/')
    
    
    return redirect('/')

# Def que nos permite cargar un animal a la base de datos
def carga_animal(request):
  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())
  ultimas_vacunaciones = Vacunacion.objects.values('id_animal_id').annotate(ultima_fecha=Max('date')).values('id_animal_id', 'ultima_fecha')
  ultimas_pariciones = Paricion.objects.values('id_animal_id').annotate(ultima_fecha=Max('date')).values('id_animal_id', 'ultima_fecha')

  if request.method == 'GET':
    return render(request, 'carga_animales.html',{
      'animales':animales,
      'vacunacion': vacunacion,
      'paricion': paricion,
      'ult_vacunacion': ultimas_vacunaciones,
      'ult_paricion': ultimas_pariciones
    })
  else :
    if ('animal' in request.POST and request.POST['animal']) and ('caravana' in request.POST and request.POST['caravana']) and ('edad' in request.POST and request.POST['edad']):
        Animales.objects.create(name=request.POST['animal'], nro_caravana=request.POST['caravana'], cant_pariciones=0,edad=request.POST['edad'])
        return redirect('/Cargar_animales/')
    
    return redirect('/Cargar_animales')

# Def que solo nos muestra los animales cargados en la base de datos
def lista_animales(request):
  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())
  ultimas_vacunaciones = Vacunacion.objects.values('id_animal_id').annotate(ultima_fecha=Max('date')).values('id_animal_id', 'ultima_fecha')
  ultimas_pariciones = Paricion.objects.values('id_animal_id').annotate(ultima_fecha=Max('date')).values('id_animal_id', 'ultima_fecha')

  buscar_c = request.GET.get('buscar_c')
  buscar_t = request.GET.get('buscar_t')
  buscar_v = request.GET.get('buscar_v')
  buscar_p = request.GET.get('buscar_p')

  # Filtro para buscar por tipo
  if buscar_t:
    animal = Animales.objects.filter(Q(name__icontains = buscar_t)).distinct()

    return render(request, 'lista_animales.html',{
      'animales': animal,
      'vacunacion': vacunacion,
      'paricion': paricion,
      'ult_vacunacion': ultimas_vacunaciones,
      'ult_paricion':ultimas_pariciones
    })

  # Filtro para buscar por caravana
  if buscar_c:
    animal = Animales.objects.filter(
      Q(nro_caravana__icontains = buscar_c)
    ).distinct()

    return render(request, 'lista_animales.html',{
      'animales': animal,
      'vacunacion': vacunacion,
      'paricion': paricion,
      'ult_vacunacion': ultimas_vacunaciones,
      'ult_paricion':ultimas_pariciones
    })

  # Filtro para buscar por fecha vacunacion
  if buscar_v:
    vacunas = Animales.objects.filter(vacunacion__date=buscar_v)

    return render( request, 'lista_animales.html',{
      'animales': vacunas,
      'vacunacion': vacunacion,
      'paricion': paricion,
      'ult_vacunacion': ultimas_vacunaciones,
      'ult_paricion': ultimas_pariciones,
    })
  
  # Filtro para buscar por fecha de paricion
  if buscar_p:
    par = Animales.objects.filter(paricion__date=buscar_p)

    return render( request, 'lista_animales.html',{
      'animales': par,
      'vacunacion': vacunacion,
      'paricion': paricion,
      'ult_vacunacion': ultimas_vacunaciones,
      'ult_paricion': ultimas_pariciones,
    })

  
  return render(request, 'lista_animales.html',{
    'animales': animales,
    'vacunacion': vacunacion,
    'paricion': paricion,
    'ult_vacunacion': ultimas_vacunaciones,
    'ult_paricion': ultimas_pariciones,
  })

# Def que funciona cuando hacemos click en editar
#     Nos permite editar el animal, la ultima fecha de vacunacion
#     ultima fecha de paricion y la descripcion de la vacunacion
def editar(request):

  animales = list(Animales.objects.values())
  vacunacion = list(Vacunacion.objects.values())
  paricion = list(Paricion.objects.values())
  lista_ult_p = Paricion.objects.values('id_animal_id').annotate(ult_fecha_paricion=Max('date'))
  lista_ult_v = Vacunacion.objects.values('id_animal_id').annotate(ult_fecha_vacunacion=Max('date'))
  ultimas_vacunaciones = Vacunacion.objects.values('id_animal_id').annotate(ultima_fecha=Max('date')).values('id_animal_id', 'ultima_fecha')
  ultimas_pariciones = Paricion.objects.values('id_animal_id').annotate(ultima_fecha=Max('date')).values('id_animal_id', 'ultima_fecha')
  
  if request.method == 'GET':
    animal = Animales.objects.get(id=request.GET['animal_id'])
    ult_p = lista_ult_p.filter(id_animal_id=request.GET['animal_id']).values('ult_fecha_paricion')
    ult_v = lista_ult_v.filter(id_animal_id=request.GET['animal_id']).values('ult_fecha_vacunacion')
    desc = lista_ult_v.filter(id_animal_id=request.GET['animal_id']).values('description')

    # Si el animal tiene fecha para editar
    if ult_v and ult_p :
      for i in ult_v:
        f = i['ult_fecha_vacunacion']

      for i in ult_p:
        p = i['ult_fecha_paricion']

      id_p = Paricion.objects.get(id_animal_id=animal.id, date=p)
      id_v = Vacunacion.objects.get(id_animal_id=animal.id, date=f)

      return render(request, 'editar_animal.html',{
      'animales':animales,
      'vacunacion':vacunacion,
      'paricion':paricion,
      'ult_p':ult_p,
      'ult_v':ult_v,
      'id_a':animal,
      'id_p':id_p,
      'id_v':id_v,
      'description':desc
      })
    # Si hay vacunacion y no hay paricion
    elif ult_v and not ult_p:
      for i in ult_v:
        f = i['ult_fecha_vacunacion']

      id_v = Vacunacion.objects.get(id_animal_id=animal.id, date=f)
      
      return render(request, 'editar_animal.html',{
      'animales':animales,
      'vacunacion':vacunacion,
      'paricion':paricion,
      'ult_p':ult_p,
      'ult_v':ult_v,
      'id_a':animal,
      'id_v':id_v,
      'description':desc
      })
    # Si no hay vacunacion y hay paricion
    elif not ult_v and ult_p:

      for i in ult_p:
        p = i['ult_fecha_paricion']

      id_p = Paricion.objects.get(id_animal_id=animal.id, date=p)

      return render(request, 'editar_animal.html',{
      'animales':animales,
      'vacunacion':vacunacion,
      'paricion':paricion,
      'ult_p':ult_p,
      'ult_v':ult_v,
      'id_a':animal,
      'id_p':id_p,
      'description':desc
      })

    return render(request, 'editar_animal.html',{
      'animales':animales,
      'vacunacion':vacunacion,
      'paricion':paricion,
      'ult_p':ult_p,
      'ult_v':ult_v,
      'id_a':animal,
      'description':desc
    })
  else:
    # Si es method = POST
    animal = Animales.objects.get(id=request.POST['id'])
    animal.nro_caravana = request.POST['nro_caravana']
    animal.save()

    if 'id_v' in request.POST and request.POST['id_v']:
      v = Vacunacion.objects.get(id=request.POST['id_v'])
      v.date = request.POST['fecha_v']
      v.description = request.POST['descripcion']
      v.save()


    if 'id_p' in request.POST and request.POST['id_p']:
      p = Paricion.objects.get(id=request.POST['id_p'])
      p.date = request.POST['fecha_p']
      p.save()

    return render(request, 'lista_animales.html',{
      'animales':animales,
      'vacunacion':vacunacion,
      'paricion':paricion,
      'ult_vacunacion': ultimas_vacunaciones,
      'ult_paricion': ultimas_pariciones
    })


# Def nos permite eliminar un animal seleccionado
def eliminar(request):
  animal = Animales.objects.get(id=request.POST['id'])
  if request.POST['eliminar'] == '1':
    Vendido.objects.create(name=animal.name, nro_caravana=animal.nro_caravana)
  else:
    Muerto.objects.create(name=animal.name, nro_caravana=animal.nro_caravana)

  animal.delete()

  return redirect('/')

def eliminar2(request):
  animal = Animales.objects.get(id=request.POST['animal_id'])
  lista_ult_p = Paricion.objects.values('id_animal_id').annotate(ult_fecha_paricion=Max('date'))
  lista_ult_v = Vacunacion.objects.values('id_animal_id').annotate(ult_fecha_vacunacion=Max('date'))
  ult_p = lista_ult_p.filter(id_animal_id=request.POST['animal_id']).values('ult_fecha_paricion')
  ult_v = lista_ult_v.filter(id_animal_id=request.POST['animal_id']).values('ult_fecha_vacunacion')
  if ult_p and ult_v:
    return render(request, 'eliminar.html',{
      'id_a':animal,
      'ult_p':ult_p,
      'ult_v':ult_v,
    })
  elif ult_p and not ult_v:
    return render(request, 'eliminar.html',{
      'id_a': animal,
      'ult_p':ult_p,
    })
  elif  not(ult_p) and ult_v:
    return render(request, 'eliminar.html',{
      'id_a': animal,
      'ult_v': ult_v,
    })
  
  return render(request, 'eliminar.html',{
    'id_a':animal,
  })

def grafico(request):

  # Creamos el gráfico del Plantel completo

  v = Animales.objects.filter(name='Vaca').count()
  t = Animales.objects.filter(name='Toro').count()
  vaq = Animales.objects.filter(name='Vaquillona').count()
  ter = Animales.objects.filter(name='Ternero').count()

  ruta = '/home/fedecai93/Documentos/djangoproyect/manejo/static/img/'
  tipos = ['Vaca', 'Vaquillona', 'Toro', 'Ternero']
  cant = [v,vaq,t,ter]
  name = 'Plantel.png'

  ret_graf(ruta,tipos,cant,name)

  # ---------------------------------------

  # Creamos el gráfico de Páriciones

  animales = Animales.objects.values()

  parieron = 0
  no_parieron = 0

  for animal in animales:
    if animal['cant_pariciones'] > 0 :
      parieron = parieron+1
    else:
      no_parieron = no_parieron+1

  tipos = ['Parieron', 'No Parieron']
  cant = [parieron, no_parieron]
  name = 'Paricion.png'
  ret_graf(ruta,tipos,cant,name)

  # ---------------------------------------

  # Creamos el gráfico de Mortandad

  vendidos = Vendido.objects.count()
  muertos = Muerto.objects.count()

  tipos = ['Muertos', 'Vendidos']
  cant = [muertos, vendidos]
  name = 'Mortandad.png'

  ret_graf(ruta, tipos,cant, name)

  return render(request, 'grafico.html',{})

def ret_graf(ruta, tipos, cantidad, name):
  fig, ax = plt.subplots()
  ax.pie(cantidad, labels=tipos, autopct='%1.1f%%')
  ruta_g = os.path.join(ruta,name)
  print(ruta_g)
  plt.savefig(ruta_g)
  plt.close()
  
  return 