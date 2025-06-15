from django.db import models

# Create your models here.
# dashboardproductos/views.py

from django.shortcuts import render
from mi_app.models import Producto, Marca, Categoria , TipoMotor, Proveedor, Cliente

def dashboard(request):
    # Ejemplo: obtener todos los productos
    productos = Producto.objects.all()

    context = {
        'productos': productos,
    }
    return render(request, 'dashboardproductos/dashboard.html', context)
