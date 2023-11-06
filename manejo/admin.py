from django.contrib import admin
from .models import Animales, Vacunacion, Paricion, Vendido, Muerto

# Register your models here.

admin.site.register(Animales)
admin.site.register(Vacunacion)
admin.site.register(Paricion)
admin.site.register(Vendido)
admin.site.register(Muerto)