from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from appProjetoH.urls import sua_funcao_de_processamento, home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appProjetoH.urls')),
    path('appProjetoJ/', sua_funcao_de_processamento, name='sua_funcao_de_processamento'),
    path('', home, name='grafico/'),
   path('enquete/', include('enquete.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
