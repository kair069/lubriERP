"""
URL configuration for Proyecto1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aplicacion/', include('mi_app.urls')),
    path('logs/', include('aplicacionLogs.urls')),
    path('dashboard/', include('myapp.urls')),  # Ruta más específica
    path('pedidos/', include('pedidos.urls')),  # Se accede a las URLs de pedidos con el prefijo /pedidos/
    path('dashboardproductos/', include('dashboardproductos.urls')),
    path('pagos/', include('pagos.urls')),
    path("api/", include("chatbot1.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
