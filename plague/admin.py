# plague/admin.py

from django.contrib import admin
from .models import Plague, PlagueType

@admin.register(Plague)
class PlagueAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'common_name', 
        'scientific_name', 
        'nomenclature', 
        'family', 
        'plague_type',  # Corrected from 'type' to 'plague_type'
        'description', 
        'control_methods', 
        'damage_symptoms', 
        'created_at', 
        'updated_at'
    )
    search_fields = (
        'name', 
        'description', 
        'common_name', 
        'scientific_name'
    )
    list_filter = (
        'family', 
        'plague_type'  # Corrected from 'type' to 'plague_type'
    )
    ordering = ('name',)

@admin.register(PlagueType)
class PlagueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
