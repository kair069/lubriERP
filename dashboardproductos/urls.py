# dashboardproductos/urls.py

from django.urls import path
from .views import stock_por_marca, stock_por_producto

urlpatterns = [
    path('stock/', stock_por_marca, name='stock_por_marca'),
    path('stock_por_producto/', stock_por_producto, name='stock_por_producto'),
]