from django.utils import timezone
from rest_framework import serializers
from .models import Persona, Lugar, Viaje


class PersonaSerializer(serializers.ModelSerializer):
    cantidad_viajes = serializers.IntegerField(source='viajes.count', read_only=True)

    class Meta:
        model = Persona
        fields = '__all__'

    def validate_fecha_nacimiento(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError('La fecha de nacimiento no puede ser futura.')
        return value


class LugarSerializer(serializers.ModelSerializer):
    cantidad_visitas = serializers.IntegerField(source='visitas.count', read_only=True)

    class Meta:
        model = Lugar
        fields = '__all__'


class PersonaResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'rut', 'nombre', 'apellido', 'foto')


class LugarResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ('id', 'nombre', 'ciudad', 'pais', 'foto')


class ViajeSerializer(serializers.ModelSerializer):
    # Escritura: IDs
    persona = serializers.PrimaryKeyRelatedField(queryset=Persona.objects.all())
    lugar = serializers.PrimaryKeyRelatedField(queryset=Lugar.objects.all())
    # Lectura: datos legibles
    persona_detalle = PersonaResumenSerializer(source='persona', read_only=True)
    lugar_detalle = LugarResumenSerializer(source='lugar', read_only=True)

    class Meta:
        model = Viaje
        fields = (
            'id', 'persona', 'lugar', 'persona_detalle', 'lugar_detalle',
            'fecha_visita', 'titulo', 'relato', 'foto', 'calificacion', 'creado',
        )
        read_only_fields = ('creado',)

    def validate_fecha_visita(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError('La fecha de visita no puede ser futura.')
        return value