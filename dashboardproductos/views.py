# # dashboardproductos/views.py

# from django.shortcuts import render
# from django.db.models import Sum
# from mi_app.models import Producto, Marca, Categoria, TipoMotor, Proveedor  # Importamos los modelos existentes

# def stock_por_marca(request):
#     # Recoger filtros desde la URL (GET)
#     categoria_filter = request.GET.get('categoria', '')
#     marca_filter = request.GET.get('marca', '')

#     # Consulta base: todos los productos
#     productos_qs = Producto.objects.all()

#     # Aplicar filtro de categoría si se seleccionó
#     if categoria_filter:
#         productos_qs = productos_qs.filter(categoria__nombre_categoria=categoria_filter)
#     # Aplicar filtro de marca si se seleccionó
#     if marca_filter:
#         productos_qs = productos_qs.filter(marca__nombre_marca=marca_filter)

#     # Agregar (group by) por marca y sumar el stock
#     data = productos_qs.values('marca__nombre_marca').annotate(total_stock=Sum('stock'))

#     # Obtener todas las categorías y marcas para los selectores del formulario
#     categorias = Categoria.objects.all()
#     marcas = Marca.objects.all()

#     context = {
#         'data': list(data),  # Convertimos a lista para facilitar su uso en el template
#         'categorias': categorias,
#         'marcas': marcas,
#     }
#     return render(request, 'dashboardproductos/stock_por_marca.html', context)


from django.shortcuts import render
from django.db.models import Sum
from mi_app.models import Producto, Marca, Categoria, TipoMotor, Proveedor

def stock_por_marca(request):
    categoria_filter = request.GET.get('categoria', '')
    marca_filter = request.GET.get('marca', '')

    productos_qs = Producto.objects.all()

    if categoria_filter:
        productos_qs = productos_qs.filter(categoria__nombre_categoria=categoria_filter)
    if marca_filter:
        productos_qs = productos_qs.filter(marca__nombre_marca=marca_filter)

    # Si se filtra por una marca, obtenemos directamente el total
    if marca_filter:
        total_stock = productos_qs.aggregate(total_stock=Sum('stock'))['total_stock']
        data = [{'marca__nombre_marca': marca_filter, 'total_stock': total_stock}]
    else:
        data = list(productos_qs.values('marca__nombre_marca').annotate(total_stock=Sum('stock')))

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()

    context = {
        'data': data,
        'categorias': categorias,
        'marcas': marcas,
    }
    return render(request, 'dashboardproductos/stock_por_marca.html', context)



# dashboardproductos/views.py

# dashboardproductos/views.py



# from django.shortcuts import render
# from django.db.models import Count, Sum
# from .models import Producto, Categoria, Marca

# def stock_por_producto(request):
#     # Recoger filtros desde la URL (GET)
#     categoria_filter = request.GET.get('categoria', '')
#     marca_filter = request.GET.get('marca', '')

#     # Consulta base con filtros aplicados
#     productos_qs = Producto.objects.all()
#     if categoria_filter:
#         productos_qs = productos_qs.filter(categoria__nombre_categoria=categoria_filter)
#     if marca_filter:
#         productos_qs = productos_qs.filter(marca__nombre_marca=marca_filter)

#     # Datos para el gráfico
#     data = [
#         {
#             'nombre_producto': producto.nombre_producto,
#             'stock': producto.stock
#         }
#         for producto in productos_qs
#     ]

#     # --- Tabla de Frecuencias ---
#     tabla_frecuencias_qs = productos_qs.values('nombre_producto', 'marca__nombre_marca').annotate(
#         frecuencia=Count('id'),
#         total_stock=Sum('stock')
#     )
#     total_frecuencia = sum(item['frecuencia'] for item in tabla_frecuencias_qs) or 1
#     total_stock_general = sum(item['total_stock'] for item in tabla_frecuencias_qs) or 1
    
#     tabla_frecuencias = [
#         {
#             'nombre_producto': item['nombre_producto'],
#             'marca': item['marca__nombre_marca'],
#             'frecuencia': item['frecuencia'],
#             'porcentaje_frecuencia': round((item['frecuencia'] * 100 / total_frecuencia), 2),
#             'total_stock': item['total_stock'],
#             'porcentaje_stock': round((item['total_stock'] * 100 / total_stock_general), 2),
#         }
#         for item in tabla_frecuencias_qs
#     ]

#     # --- KPI de Stock ---
#     kpi_stock = productos_qs.aggregate(total_stock=Sum('stock'))['total_stock'] or 0

#     # Obtener categorías y marcas
#     categorias = Categoria.objects.order_by('nombre_categoria')
#     marcas = Marca.objects.order_by('nombre_marca')

#     context = {
#         'data': data,
#         'tabla_frecuencias': tabla_frecuencias,
#         'kpi_stock': kpi_stock,
#         'categorias': categorias,
#         'marcas': marcas,
#         'selected_categoria': categoria_filter,
#         'selected_marca': marca_filter,
#     }
    
#     return render(request, 'dashboardproductos/stock_por_producto.html', context)



################################################################################################MEJORA



from django.shortcuts import render
from django.db.models import Count, Sum, F, Q
from django.core.paginator import Paginator
from .models import Producto, Categoria, Marca

def stock_por_producto(request):
    # Recoger filtros desde la URL (GET)
    categoria_filter = request.GET.get('categoria', '')
    marca_filter = request.GET.get('marca', '')
    search_query = request.GET.get('search', '')
    stock_min = request.GET.get('stock_min', '')
    
    # Consulta base con filtros aplicados y optimización con select_related
    productos_qs = Producto.objects.select_related('categoria', 'marca', 'tipo_motor')
    
    # Aplicar filtros
    filters = Q()
    if categoria_filter:
        filters &= Q(categoria__nombre_categoria=categoria_filter)
    if marca_filter:
        filters &= Q(marca__nombre_marca=marca_filter)
    if search_query:
        filters &= Q(nombre_producto__icontains=search_query)
    if stock_min and stock_min.isdigit():
        filters &= Q(stock__lte=int(stock_min))
    
    productos_qs = productos_qs.filter(filters)

    # Datos para el gráfico - Limitamos a los 15 productos con menos stock para mayor claridad
    productos_grafico = productos_qs.order_by('stock')[:15]
    data = [
        {
            'nombre_producto': producto.nombre_producto,
            'stock': producto.stock,
            'marca': producto.marca.nombre_marca,
            'categoria': producto.categoria.nombre_categoria
        }
        for producto in productos_grafico
    ]

    # --- Tabla de Frecuencias ---
    tabla_frecuencias_qs = productos_qs.values(
        'nombre_producto', 
        'marca__nombre_marca', 
        'categoria__nombre_categoria'
    ).annotate(
        frecuencia=Count('id'),
        total_stock=Sum('stock')
    ).order_by('-total_stock')
    
    # Paginación para la tabla
    paginator = Paginator(list(tabla_frecuencias_qs), 10)  # 10 items por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Cálculos de totales para porcentajes
    total_frecuencia = sum(item['frecuencia'] for item in tabla_frecuencias_qs) or 1
    total_stock_general = sum(item['total_stock'] for item in tabla_frecuencias_qs) or 1
    
    tabla_frecuencias = [
        {
            'nombre_producto': item['nombre_producto'],
            'marca': item['marca__nombre_marca'],
            'categoria': item['categoria__nombre_categoria'],
            'frecuencia': item['frecuencia'],
            'porcentaje_frecuencia': round((item['frecuencia'] * 100 / total_frecuencia), 2),
            'total_stock': item['total_stock'],
            'porcentaje_stock': round((item['total_stock'] * 100 / total_stock_general), 2),
            'alerta': 'danger' if item['total_stock'] <= 10 else ('warning' if item['total_stock'] <= 20 else '')
        }
        for item in page_obj.object_list
    ]

    # --- KPIs mejorados ---
    kpi_data = productos_qs.aggregate(
        total_stock=Sum('stock'),
        total_productos=Count('id'),
        productos_sin_stock=Count('id', filter=Q(stock=0)),
        productos_stock_bajo=Count('id', filter=Q(stock__gt=0, stock__lte=10))
    )
    
    # Verificar si hay productos con stock crítico
    has_critical_stock = any(item['alerta'] == 'danger' for item in tabla_frecuencias)

    # Obtener categorías y marcas
    categorias = Categoria.objects.order_by('nombre_categoria')
    marcas = Marca.objects.order_by('nombre_marca')

    # Construir query string para paginación manteniendo filtros
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    current_filters = query_params.urlencode()

    context = {
        'data': data,
        'tabla_frecuencias': tabla_frecuencias,
        'kpis': kpi_data,
        'categorias': categorias,
        'marcas': marcas,
        'selected_categoria': categoria_filter,
        'selected_marca': marca_filter,
        'search_query': search_query,
        'stock_min': stock_min,
        'page_obj': page_obj,
        'current_filters': current_filters,
        'has_critical_stock': has_critical_stock
    }
    
    return render(request, 'dashboardproductos/stock_por_producto.html', context)