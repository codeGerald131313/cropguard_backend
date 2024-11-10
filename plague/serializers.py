# serializers.py
from rest_framework import serializers
from .models import Plague, PlagueType

class PlagueTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlagueType
        fields = ['id']  # Solo el ID para la creación

# Serializador para la creación de plagas
class PlagueCreateSerializer(serializers.ModelSerializer):
    plague_type = serializers.PrimaryKeyRelatedField(queryset=PlagueType.objects.all())

    class Meta:
        model = Plague
        fields = [
            'id', 'name', 'common_name', 'scientific_name', 
            'nomenclature', 'family', 'plague_type', 
            'description', 'control_methods', 'damage_symptoms'
        ]

    def create(self, validated_data):
        plague_type = validated_data.pop('plague_type')
        plague = Plague.objects.create(plague_type=plague_type, **validated_data)
        return plague

class PlagueUpdateSerializer(serializers.ModelSerializer):
    plague_type = serializers.PrimaryKeyRelatedField(queryset=PlagueType.objects.all())  # Acepta solo el ID

    class Meta:
        model = Plague
        fields = ['id', 'name', 'common_name', 'scientific_name', 'nomenclature', 'family', 'plague_type', 'description', 'control_methods', 'damage_symptoms']

    def update(self, instance, validated_data):
        # Actualizar todos los campos recibidos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    
class PlagueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlagueType
        fields = ['id', 'name']

class PlagueSerializer(serializers.ModelSerializer):
    plague_type = PlagueTypeSerializer()  # Serializa el objeto completo

    class Meta:
        model = Plague
        fields = ['id', 'name', 'common_name', 'scientific_name', 'nomenclature', 'family', 'plague_type', 'description', 'control_methods', 'damage_symptoms']

