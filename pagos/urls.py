from django.urls import path
from .views import (
    ArbitriosMunicipalesListView, ArbitriosMunicipalesDetailView,
    ArbitriosMunicipalesCreateView, ArbitriosMunicipalesUpdateView, 
    ArbitriosMunicipalesDeleteView
)

urlpatterns = [
    path('', ArbitriosMunicipalesListView.as_view(), name='arbitrios_lista'),
    path('<int:pk>/', ArbitriosMunicipalesDetailView.as_view(), name='arbitrios_detalle'),
    path('nuevo/', ArbitriosMunicipalesCreateView.as_view(), name='arbitrios_nuevo'),
    path('<int:pk>/editar/', ArbitriosMunicipalesUpdateView.as_view(), name='arbitrios_editar'),
    path('<int:pk>/eliminar/', ArbitriosMunicipalesDeleteView.as_view(), name='arbitrios_eliminar'),
]
