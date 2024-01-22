# projetoH/urls.py
from django.contrib import admin
from django.urls import path, include
from appProjetoH.views import home, sua_funcao_de_processamento
from . import views
from .views import salvar_resultado_enquete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('processamento/', sua_funcao_de_processamento, name='sua_funcao_de_processamento'),
    path('salvar_resultado_enquete/', salvar_resultado_enquete, name='salvar_resultado_enquete'),
    # outras rotas do seu aplicativo aqui...    
]

# Adicione as seguintes linhas para servir arquivos estáticos durante o desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
