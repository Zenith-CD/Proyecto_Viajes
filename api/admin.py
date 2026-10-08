from django.contrib import admin
from .models import Persona, Lugar, Viaje


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'email')
    search_fields = ('rut', 'nombre', 'apellido', 'email')


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'pais')
    search_fields = ('nombre', 'ciudad', 'pais')


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'persona', 'lugar', 'fecha_visita', 'calificacion', 'creado')
    list_filter = ('calificacion', 'lugar')