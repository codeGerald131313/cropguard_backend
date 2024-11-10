# plague/views.py
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Plague, PlagueType
from .serializers import PlagueSerializer, PlagueTypeSerializer, PlagueCreateSerializer, PlagueUpdateSerializer
import cv2
from django.conf import settings
from django.http import JsonResponse
from .utils import predict_plague  # Asumiendo que guardaste la función en un archivo utils.py
from .tasks import send_prediction_to_websocket
from .utils import class_names_dict  # Asegúrate de ajustar el import según la estructura de tu proyecto
from .models import Prediction  # Importa el modelo Prediction

class PlagueListView(APIView):
    def get(self, request):
        plagues = Plague.objects.all()
        serializer = PlagueSerializer(plagues, many=True)
        return Response({
            'status': 'success',
            'message': 'Plagues retrieved successfully',
            'data': serializer.data
        })

class PlagueTypeListView(APIView):
    def get(self, request):
        plague_types = PlagueType.objects.all()
        serializer = PlagueTypeSerializer(plague_types, many=True)
        return Response({
            'status': 'success',
            'message': 'Plague types retrieved successfully',
            'data': serializer.data
        })

class PlagueDetailView(APIView):
    def get(self, request, pk):
        try:
            plague = Plague.objects.get(pk=pk)
            serializer = PlagueSerializer(plague)
            return Response({
                'status': 'success',
                'message': 'Plague details retrieved successfully',
                'data': serializer.data
            })
        except Plague.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Plague not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

class PlagueCreateView(APIView):
    def post(self, request):
        serializer = PlagueCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Plague created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Failed to create plague',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PlagueUpdateView(APIView):
    def put(self, request, pk):
        try:
            plague = Plague.objects.get(pk=pk)
            serializer = PlagueUpdateSerializer(plague, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Plague updated successfully',
                    'data': serializer.data
                })
            return Response({
                'status': 'error',
                'message': 'Failed to update plague',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Plague.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Plague not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

class PlagueDeleteView(APIView):
    def delete(self, request, pk):
        try:
            plague = Plague.objects.get(pk=pk)
            plague.delete()
            return Response({
                'status': 'success',
                'message': 'Plague deleted successfully',
                'data': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Plague.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Plague not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

class PredictPlagueView(APIView):
    def post(self, request, *args, **kwargs):
        # Cargar el modelo
        model = tf.keras.models.load_model(settings.MODEL_PATH)
        
        # Verifica si hay archivos en la solicitud
        if not request.FILES.getlist('file'):
            return Response({"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Inicializar lista para almacenar predicciones
        predictions_list = []
        
        # Iterar sobre los archivos proporcionados
        files = request.FILES.getlist('file')
        for file in files:
            # Lee cada imagen desde el archivo
            image = Image.open(file).convert('RGB')
            img_array = np.array(image)
            img_array = tf.image.resize(img_array, (64, 64))  # Cambia a (64, 64) según el tamaño esperado por tu modelo
            img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión adicional para el batch
            
            # Realiza la predicción
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions, axis=1)[0].item()  # Convertir a int estándar
            predicted_class_name = class_names_dict[predicted_class_index]
            
            # Obtener la confianza (probabilidad) de la predicción
            confidence = np.max(predictions) * 100
            
            # Determinar el color del texto basado en la confianza
            text_color = 'green' if confidence >= 80 else 'red'
            
            # Guardar la predicción en la base de datos
            prediction = Prediction.objects.create(
                class_index=predicted_class_index,
                predicted_class=predicted_class_name,
                confidence=confidence,
                color=text_color
            )
            
            # Agregar la predicción a la lista
            prediction_data = {
                "class_index": predicted_class_index,
                "predicted_class": predicted_class_name,
                "confidence": f"{confidence:.2f}%",
                "color": text_color
            }
            predictions_list.append(prediction_data)
        
        # Enviar los resultados de todas las predicciones a través del WebSocket
        for prediction in predictions_list:
            send_prediction_to_websocket(prediction)
        
        # Retornar la respuesta HTTP con todas las predicciones
        return Response(predictions_list)


class ListPredictionsView(APIView):
    def get(self, request, *args, **kwargs):
        # Capturar los class_index que se pasan en la solicitud (por ejemplo, como parámetros de consulta)
        class_indexes = request.query_params.getlist('class_index')
        
        if not class_indexes:
            return Response({"error": "No class_index provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir los class_indexes a enteros
        try:
            class_indexes = [int(index) for index in class_indexes]
        except ValueError:
            return Response({"error": "Invalid class_index format"}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar las predicciones que coincidan con los class_index proporcionados
        predictions = Prediction.objects.filter(class_index__in=class_indexes)
        
        # Obtener los detalles de las plagas correspondientes a cada class_index
        plague_details = []
        for prediction in predictions:
            # Busca la plaga correspondiente con el class_index de la predicción
            plague = Plague.objects.filter(id=prediction.class_index).first()
            if plague:
                plague_data = {
                    "prediction_id": prediction.id,
                    "predicted_class": prediction.predicted_class,
                    "confidence": prediction.confidence,
                    "color": prediction.color,
                    "plague_name": plague.name,
                    "common_name": plague.common_name,
                    "scientific_name": plague.scientific_name,
                    "nomenclature": plague.nomenclature,
                    "family": plague.family,
                    "plague_type": plague.plague_type.name,
                    "description": plague.description,
                    "control_methods": plague.control_methods,
                    "damage_symptoms": plague.damage_symptoms
                }
                plague_details.append(plague_data)
        
        return Response(plague_details)