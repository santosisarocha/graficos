# enquete/views.py

from django.shortcuts import render

def minha_view(request):
    # Implemente sua lógica de visualização aqui
    return render(request, 'index.html')
