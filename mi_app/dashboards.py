from django.shortcuts import render
from django.db.models import Count, Avg, Max, Min, Sum, F, Q
from .models import Producto, Marca, Categoria

def dashboard_view(request):
    # 1. Distribución de Productos por Categoría
    distribucion_por_categoria = (
        Producto.objects.values('categoria__nombre_categoria')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # 2. Productos con Stock Bajo (e.g., stock menor a 10)
    stock_bajo = Producto.objects.filter(stock__lt=10).count()

    # 3. Número Total de Productos
    total_productos = Producto.objects.count()

    # 4. Productos con Precios Altos (e.g., precio mayor a 1000)
    precios_altos = Producto.objects.filter(precio__gt=1000).count()

    # 5. Distribución de Productos por Marca
    distribucion_por_marca = (
        Producto.objects.values('marca__nombre_marca')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    context = {
        'distribucion_por_categoria': distribucion_por_categoria,
        'stock_bajo': stock_bajo,
        'total_productos': total_productos,
        'precios_altos': precios_altos,
        'distribucion_por_marca': distribucion_por_marca,
    }

    return render(request, 'dashboard.html', context)
from django.shortcuts import render
from django.db.models import Count, Avg, Max, Min, Sum, F, Q
from .models import Producto, Marca, Categoria

def dashboard_view(request):
    # 1. Distribución de Productos por Categoría
    distribucion_por_categoria = (
        Producto.objects.values('categoria__nombre_categoria')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # 2. Productos con Stock Bajo (e.g., stock menor a 10)
    stock_bajo = Producto.objects.filter(stock__lt=10).count()

    # 3. Número Total de Productos
    total_productos = Producto.objects.count()

    # 4. Productos con Precios Altos (e.g., precio mayor a 1000)
    precios_altos = Producto.objects.filter(precio__gt=1000).count()

    # 5. Distribución de Productos por Marca
    distribucion_por_marca = (
        Producto.objects.values('marca__nombre_marca')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    context = {
        'distribucion_por_categoria': distribucion_por_categoria,
        'stock_bajo': stock_bajo,
        'total_productos': total_productos,
        'precios_altos': precios_altos,
        'distribucion_por_marca': distribucion_por_marca,
    }

    return render(request, 'mi_app/calculadora/dashboard.html', context) 