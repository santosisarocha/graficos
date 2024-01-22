# enquete/urls.py

from django.urls import path
from . import views
from .views import minha_view

urlpatterns = [
    path('minha-rota/', minha_view, name='minha-view'),
]
