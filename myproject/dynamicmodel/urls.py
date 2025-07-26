from django.urls import path
from .views import create_model_view

urlpatterns = [
    path('create/', create_model_view, name='create-model'),
]
