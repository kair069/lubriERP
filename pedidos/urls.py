from django.urls import path
from .views import (
    PedidoListView,
    PedidoCombinedDetailView,  # Vista combinada en lugar de PedidoDetailView
    PedidoCreateView,
    PedidoUpdateView,
    PedidoDeleteView,
    DetallePedidoListView,
    DetallePedidoDetailView,
    DetallePedidoCreateView,
    DetallePedidoUpdateView,
    DetallePedidoDeleteView,
    obtener_precio_producto,
    
)

urlpatterns = [
    # Rutas para Pedido
    path('pedido/', PedidoListView.as_view(), name='pedido_list'),
    path('pedido/<int:pk>/detalle/', PedidoCombinedDetailView.as_view(), name='pedido_combined_detail'),
    path('pedido/nuevo/', PedidoCreateView.as_view(), name='pedido_create'),
    path('pedido/<int:pk>/editar/', PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedido/<int:pk>/eliminar/', PedidoDeleteView.as_view(), name='pedido_delete'),

    # Rutas para DetallePedido
    # Lista de detalles para un pedido específico (se espera que se pase el id del pedido)
    path('pedido/<int:pedido_id>/detalles/', DetallePedidoListView.as_view(), name='detallepedido_list'),
    path('detalle/<int:pk>/', DetallePedidoDetailView.as_view(), name='detallepedido_detail'),
    
    # Crear un nuevo detalle para un pedido específico
    path('pedido/<int:pedido_id>/detalle/nuevo/', DetallePedidoCreateView.as_view(), name='detallepedido_create'),
    
    path('detalle/<int:pk>/editar/', DetallePedidoUpdateView.as_view(), name='detallepedido_update'),
    path('detalle/<int:pk>/eliminar/', DetallePedidoDeleteView.as_view(), name='detallepedido_delete'),

    path('obtener-precio-producto/', obtener_precio_producto, name='obtener_precio_producto'),
]
