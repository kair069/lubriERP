from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Producto, Categoria
from django.core.paginator import Paginator  # Asegúrate de importar Paginator
from django.shortcuts import render
from .models import Producto, Categoria


def calculadora(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    # Filtro por nombre del producto
    nombre_producto = request.GET.get('nombre', None)
    categoria_id = request.GET.get('categoria', None)
    
    if nombre_producto:
        productos = productos.filter(nombre_producto__icontains=nombre_producto)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    # Lógica para desfiltrar (vaciar filtros)
    if 'desfiltrar' in request.GET:
        nombre_producto = None
        categoria_id = None
        productos = Producto.objects.all()  # Mostrar todos los productos

    # Lógica de agregar al carrito
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            producto_id = request.POST.get('id_producto')
            # Aquí agregamos el producto al carrito (puedes usar sesión o base de datos)
            carrito = request.session.get('carrito', [])
            if producto_id not in carrito:
                carrito.append(producto_id)
                request.session['carrito'] = carrito
        elif action == 'remove':
            producto_id = request.POST.get('id_producto')
            carrito = request.session.get('carrito', [])
            if producto_id in carrito:
                carrito.remove(producto_id)
                request.session['carrito'] = carrito

    # Obtener los productos seleccionados en el carrito
    productos_seleccionados = request.session.get('carrito', [])

    # Configuración de la paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calcular el total (puedes ajustar el cálculo)
    total = 0
    for producto in productos:
        if str(producto.id) in productos_seleccionados:
            total += producto.precio

    return render(request, 'mi_app/calculadora/calculadora.html', {
        'productos': page_obj,
        'categorias': categorias,
        'total': total,
        'productos_seleccionados': productos_seleccionados,
        'nombre_producto': nombre_producto,
        'categoria_id': categoria_id,
    })
