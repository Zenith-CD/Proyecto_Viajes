from django.shortcuts import render

from rest_framework import viewsets
from .models import Persona, Lugar, Viaje
from .serializers import PersonaSerializer, LugarSerializer, ViajeSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class LugarViewSet(viewsets.ModelViewSet):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer


class ViajeViewSet(viewsets.ModelViewSet):
    serializer_class = ViajeSerializer

    def get_queryset(self):
        qs = Viaje.objects.select_related('persona', 'lugar')
        lugar = self.request.query_params.get('lugar')
        persona = self.request.query_params.get('persona')
        if lugar and lugar.isdigit():
            qs = qs.filter(lugar_id=lugar)
        if persona and persona.isdigit():
            qs = qs.filter(persona_id=persona)
        return qs