from django.db import models

class PlagueType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Plague(models.Model):
    id = models.PositiveIntegerField(primary_key=True)  # Permite valores manuales para el ID
    name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    nomenclature = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    plague_type = models.ForeignKey(PlagueType, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    control_methods = models.JSONField(blank=True, null=True)  # Cambiado a JSONField
    damage_symptoms = models.JSONField(blank=True, null=True)   # Cambiado a JSONField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.common_name
    
class Prediction(models.Model):
    class_index = models.IntegerField()
    predicted_class = models.CharField(max_length=255)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)  # Ej. 99.99
    color = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)  # Para guardar el tiempo de la predicción
    
    def __str__(self):
        return f"{self.predicted_class} - {self.confidence}%"
