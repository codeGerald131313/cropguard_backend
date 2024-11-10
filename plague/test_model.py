import os
import sys
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cropguard_backend.settings')
django.setup()

from django.conf import settings
import tensorflow as tf

# Ruta al modelo Faster R-CNN desde el path local configurado
model_path = settings.MODEL_PATH_DETECTION
model = tf.saved_model.load(model_path)

# Imprimir las firmas disponibles
print(model.signatures)
