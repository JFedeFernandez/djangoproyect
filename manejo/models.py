from django.db import models

# Create your models here.

class Animales(models.Model):
  id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=100, verbose_name="Animal")
  nro_caravana = models.IntegerField(verbose_name="Número de caravana")
  cant_pariciones = models.IntegerField(verbose_name="Cant paricion", blank=True, null=True)
  
  def __str__(self):
    return self.name + '-' + str(self.nro_caravana)

class Vacunacion(models.Model):
  id = models.BigAutoField(primary_key=True)
  date = models.DateField(verbose_name="Fecha")
  description = models.TextField(verbose_name="Descripción", blank=True, null=True)
  id_animal = models.ForeignKey(Animales, on_delete=models.CASCADE)

class Paricion(models.Model):
  id = models.BigAutoField(primary_key=True)
  date = models.DateField(verbose_name="Fecha")
  id_animal = models.ForeignKey(Animales, on_delete=models.CASCADE)