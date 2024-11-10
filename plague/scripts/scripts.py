from plague.models import Plague, PlagueType

# Diccionario de clases proporcionado ajustado para que los IDs empiecen desde 1
class_names_dict = {
    1: 'rice leaf roller',
    2: 'rice leaf caterpillar',
    3: 'paddy stem maggot',
    4: 'asiatic rice borer',
    5: 'yellow rice borer',
    6: 'rice gall midge',
    7: 'Rice Stemfly',
    8: 'brown plant hopper',
    9: 'white backed plant hopper',
    10: 'small brown plant hopper',
    11: 'rice water weevil',
    12: 'rice leafhopper',
    13: 'grain spreader thrips',
    14: 'rice shell pest',
    15: 'grub'
}

# Obtener el tipo de plaga por defecto o uno existente
plague_type = PlagueType.objects.get_or_create(name="Default Type", description="Descripción por defecto")[0]

# Datos de ejemplo para control_methods y damage_symptoms
control_methods_example = {
    1: ['Insecticide', 'Biological Control'],
    2: ['Manual Removal', 'Insecticide'],
    3: ['Soil Treatment', 'Pesticides'],
    4: ['Chemical Control', 'Biological Control'],
    5: ['Insecticides', 'Cultural Control'],
    6: ['Pesticides', 'Cultural Practices'],
    7: ['Chemical Treatment', 'Integrated Pest Management'],
    8: ['Insecticides', 'Cultural Control'],
    9: ['Pesticides', 'Biological Control'],
    10: ['Insecticides', 'Mechanical Control'],
    11: ['Soil Treatments', 'Chemical Control'],
    12: ['Insecticides', 'Cultural Methods'],
    13: ['Pesticides', 'Biological Control'],
    14: ['Chemical Control', 'Cultural Practices'],
    15: ['Manual Removal', 'Chemical Treatment']
}

damage_symptoms_example = {
    1: ['Rolled Leaves', 'Defoliation'],
    2: ['Leaf Damage', 'Caterpillar Trails'],
    3: ['Stem Damage', 'Wilted Plants'],
    4: ['Borer Holes', 'Stunted Growth'],
    5: ['Borer Damage', 'Discolored Leaves'],
    6: ['Galls on Leaves', 'Stunted Growth'],
    7: ['Leaf Damage', 'Wilted Plants'],
    8: ['Brown Spots', 'Leaf Drop'],
    9: ['White Spots', 'Leaf Curling'],
    10: ['Brown Spots', 'Leaf Drop'],
    11: ['Leaf Damage', 'Root Damage'],
    12: ['Leaf Hopping', 'Stunted Growth'],
    13: ['Leaf Spots', 'Distorted Growth'],
    14: ['Shell Damage', 'Leaf Drop'],
    15: ['Grub Damage', 'Root Damage']
}

# Registrar todos los datos en la tabla Plague
for key, value in class_names_dict.items():
    Plague.objects.update_or_create(
        id=key,  # Establecemos el id manualmente
        defaults={
            'name': value,
            'common_name': value,  # Puedes ajustar esto según necesites
            'description': f"Plaga {value}",
            'plague_type': plague_type,  # Asignamos el tipo de plaga por defecto
            'control_methods': control_methods_example.get(key, []),
            'damage_symptoms': damage_symptoms_example.get(key, [])
        }
    )

print("Primeros 15 registros insertados exitosamente.")
