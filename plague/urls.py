# plague/urls.py

from django.urls import path
from .views import PlagueListView, PlagueDetailView, PlagueCreateView, PlagueUpdateView, PlagueDeleteView, PlagueTypeListView, PredictPlagueView

urlpatterns = [
    path('plagues/', PlagueListView.as_view(), name='plague-list'),
    path('plagues/<int:pk>/', PlagueDetailView.as_view(), name='plague-detail'),
    path('plagues/create/', PlagueCreateView.as_view(), name='plague-create'), 
    path('plagues/update/<int:pk>/', PlagueUpdateView.as_view(), name='plague-update'),
    path('plagues/delete/<int:pk>/', PlagueDeleteView.as_view(), name='plague-delete'),
    path('plague-types/', PlagueTypeListView.as_view(), name='plague-type-list'), 
    path('predict-plague/', PredictPlagueView.as_view(), name='predict-plague'),
 
]
