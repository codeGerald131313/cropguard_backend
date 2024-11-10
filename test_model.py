import tensorflow as tf
import tensorflow_hub as hub

# Cargar el modelo desde TensorFlow Hub
model_url = 'https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1'
model = hub.load(model_url)

# Imprimir las firmas disponibles
print("Signatures:", model.signatures)
