from django.shortcuts import render

from django.shortcuts import render

from mi_app.utils import generar_numero_documento

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F, Q
from django.utils import timezone
from datetime import timedelta

# Importa tus modelos
from .models import (
    Producto, Cliente, Proveedor, Venta, Compra, Marca, 
    Categoria, DetalleVenta, DetalleCompra, CambioAceite
)


def home(request):
    # Fechas para cálculos
    hoy = timezone.now()
    inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    hace_30_dias = hoy - timedelta(days=30)
    hace_7_dias = hoy - timedelta(days=7)
    
    # Estadísticas básicas del sistema
    stats = {
        'total_productos': Producto.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'total_proveedores': Proveedor.objects.count(),
        'total_ventas': Venta.objects.count(),
        'total_marcas': Marca.objects.count(),
        'total_categorias': Categoria.objects.count(),
    }
    
    # Productos con stock bajo (menos de 5 unidades)
    productos_stock_bajo = Producto.objects.filter(stock__lt=5).count()
    stats['productos_stock_bajo'] = productos_stock_bajo
    
    # Ventas recientes para la sección de actividad
    ventas_recientes = Venta.objects.all().order_by('-fecha_venta')[:5]
    
    # Compras recientes para la sección de actividad
    compras_recientes = Compra.objects.all().order_by('-fecha_compra')[:5]
    
    # Cambios de aceite recientes
    cambios_aceite_recientes = CambioAceite.objects.all().order_by('-fecha_cambio')[:5]
    
    # Actividades recientes combinadas
    actividades_recientes = []
    
    # Añadir ventas a actividades
    for venta in ventas_recientes:
        actividades_recientes.append({
            'tipo': 'venta',
            'titulo': f'Venta #{venta.numero_documento}',
            'descripcion': f'Venta a {venta.cliente_nombre} por S/. {venta.total_venta}',
            'fecha': venta.fecha_venta,
            'icono': 'fa-file-invoice-dollar',
            'color': 'text-success'
        })
    
    # Añadir compras a actividades
    for compra in compras_recientes:
        actividades_recientes.append({
            'tipo': 'compra',
            'titulo': f'Compra #{compra.id}',
            'descripcion': f'Compra a {compra.proveedor.nombre_proveedor} por S/. {compra.total_compra}',
            'fecha': compra.fecha_compra,
            'icono': 'fa-shopping-cart',
            'color': 'text-primary'
        })
    
    # Añadir cambios de aceite a actividades
    for cambio in cambios_aceite_recientes:
        actividades_recientes.append({
            'tipo': 'cambio_aceite',
            'titulo': f'Cambio de Aceite',
            'descripcion': f'Cliente: {cambio.cliente.nombre_cliente}, Tipo: {cambio.tipo_aceite}',
            'fecha': cambio.fecha_cambio,
            'icono': 'fa-oil-can',
            'color': 'text-warning'
        })
    
    # Ordenar actividades por fecha (más reciente primero)
    actividades_recientes = sorted(
        actividades_recientes, 
        key=lambda x: x['fecha'], 
        reverse=True
    )[:10]  # Limitar a 10 actividades más recientes
    
    # Calcular ventas y compras del último mes para gráficos/estadísticas
    ventas_mes = Venta.objects.filter(fecha_venta__gte=inicio_mes).aggregate(
        total=Sum('total_venta')
    )['total'] or 0
    
    compras_mes = Compra.objects.filter(fecha_compra__gte=inicio_mes).aggregate(
        total=Sum('total_compra')
    )['total'] or 0
    
    # Top 5 productos más vendidos
    top_productos = DetalleVenta.objects.values(
        'producto__nombre_producto'
    ).annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]
    
    # Top 5 clientes con más compras
    top_clientes = Venta.objects.values(
        'cliente__nombre_cliente'
    ).annotate(
        total_compras=Count('id'),
        monto_total=Sum('total_venta')
    ).order_by('-total_compras')[:5]
    
    context = {
        'usuario': request.user,
        'stats': stats,
        'actividades_recientes': actividades_recientes,
        'ventas_mes': ventas_mes,
        'compras_mes': compras_mes,
        'balance_mes': ventas_mes - compras_mes,
        'top_productos': top_productos,
        'top_clientes': top_clientes,
    }
    
    return render(request, 'mi_app/home.html', context)

def about(request):
    return render(request, 'mi_app/about.html')

def contact(request):
    return render(request, 'mi_app/contact.html')


  
#3♣3♣35#3♣3♣35353535#                                      MARCAS

from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca
from .forms import AgregarProductoForm, MarcaForm

# Vista para crear una nueva marca
def crear_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_marcas')  # Redirigir a la lista de marcas
    else:
        form = MarcaForm()
    return render(request, 'mi_app/marcas/crear_marca.html', {'form': form})

# Vista para listar todas las marcas
def listar_marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'mi_app/marcas/listar_marcas.html', {'marcas': marcas})

# Vista para actualizar una marca existente
def actualizar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('listar_marcas')  # Redirigir a la lista de marcas
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'mi_app/marcas/actualizar_marca.html', {'form': form, 'marca': marca})

# Vista para eliminar una marca
def eliminar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('listar_marcas')  # Redirigir a la lista de marcas
    return render(request, 'mi_app/marcas/eliminar_marca.html', {'marca': marca})



#3♣3♣35#3♣3♣35353535#                                      CATEGORIAS

from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'mi_app/categorias/listar_categorias.html', {'categorias': categorias})


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')  # Asegúrate de tener una URL configurada
    else:
        form = CategoriaForm()
    
    return render(request, 'mi_app/categorias/crear_categoria.html', {'form': form})



def actualizar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'mi_app/categorias/actualizar_categoria.html', {'form': form})


def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    
    return render(request, 'mi_app/categorias/eliminar_categoria.html', {'categoria': categoria})


#3♣3♣35#3♣3♣35353535#                                      tipo moto
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TipoMotor
from .forms import TipoMotorForm

# Listar Tipos de Motor
def listar_tipos_motor(request):
    tipos_motor = TipoMotor.objects.all()
    return render(request, 'mi_app/tipomotor/listar.html', {'tipos_motor': tipos_motor})

# Crear Tipo de Motor
def crear_tipo_motor(request):
    if request.method == 'POST':
        form = TipoMotorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de motor creado exitosamente.')
            return redirect('listar_tipos_motor')
        else:
            messages.error(request, 'Hubo un error al crear el tipo de motor.')
    else:
        form = TipoMotorForm()
    return render(request, 'mi_app/tipomotor/form.html', {'form': form})

# Editar Tipo de Motor
def editar_tipo_motor(request, pk):
    tipo_motor = get_object_or_404(TipoMotor, pk=pk)
    if request.method == 'POST':
        form = TipoMotorForm(request.POST, instance=tipo_motor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de motor actualizado correctamente.')
            return redirect('listar_tipos_motor')
        else:
            messages.error(request, 'Hubo un error al actualizar el tipo de motor.')
    else:
        form = TipoMotorForm(instance=tipo_motor)
    return render(request, 'mi_app/tipomotor/form.html', {'form': form})

# Eliminar Tipo de Motor
def eliminar_tipo_motor(request, pk):
    tipo_motor = get_object_or_404(TipoMotor, pk=pk)
    if request.method == 'POST':
        tipo_motor.delete()
        messages.success(request, 'Tipo de motor eliminado exitosamente.')
        return redirect('listar_tipos_motor')
    return render(request, 'mi_app/tipomotor/confirmar_eliminar.html', {'tipo_motor': tipo_motor})


#3♣3♣35#3♣3♣35353535#                                      producto

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Marca, Categoria, TipoMotor
from .forms import ProductoForm

# Listar Productos

# def listar_productos(request):
#     productos = Producto.objects.select_related('marca', 'categoria', 'tipo_motor').all()
#     return render(request, 'mi_app/producto/listar.html', {'productos': productos})

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Producto

# def listar_productos(request):
#     # Inicializar la consulta básica para seleccionar relaciones de los productos
#     productos_list = Producto.objects.select_related('marca', 'categoria', 'tipo_motor')

#      # Obtener los parámetros de búsqueda desde la solicitud GET
#     nombre = request.GET.get('nombre', '')
#     marca = request.GET.get('marca', '')
#     qr_code = request.GET.get('qr_code', '')
#     categoria = request.GET.get('categoria', '')

#      # Crear un filtro dinámico usando Q para poder combinar condiciones
#     filtros = Q()
#     # Aplicar filtros solo si tienen valor
#     if nombre:
#         filtros &= Q(nombre_producto__icontains=nombre)  # Filtrar por nombre del producto
#     if marca:
#         filtros &= Q(marca__nombre_marca__icontains=marca)  # Filtrar por nombre de la marca
#     if qr_code:
#         filtros &= Q(qr_code__icontains=qr_code)  # Filtrar por código QR
#     if categoria:
#         filtros &= Q(categoria__nombre_categoria__icontains=categoria)  # Filtrar por nombre de categoría


#     # Aplicar los filtros solo si se han añadido
#     if filtros != Q():
#         productos_list = productos_list.filter(filtros)

#     # Paginación: 4 productos por página
#     paginator = Paginator(productos_list, 4)
#     page = request.GET.get('page')

#     try:
#         productos = paginator.get_page(page)
#     except:
#         productos = paginator.get_page(1)  # Si la página no es válida, cargar la primera página

#     # Mantener los filtros en la URL para la paginación
#     base_url = '?'
#     if nombre:
#         base_url += f'nombre={nombre}&'
#     if marca:
#         base_url += f'marca={marca}&'
#     if qr_code:
#         base_url += f'qr_code={qr_code}&'

#     # Eliminar el último '&' si existe
#     if base_url.endswith('&'):
#         base_url = base_url[:-1]

#     marcas = Marca.objects.all()
#     categorias = Categoria.objects.all()
#     return render(request, 'mi_app/producto/listar.html', {
#         'productos': productos,
#         'nombre': nombre,
#         'marca': marca,
#         'qr_code': qr_code,
#         'categoria': categoria,
#         'marcas': marcas,
#         'categorias': categorias,
#     })
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto, Marca, Categoria

def listar_productos(request):
    # Inicializar la consulta básica
    productos_list = Producto.objects.select_related('marca', 'categoria', 'tipo_motor')
    
    # Obtener los parámetros de búsqueda
    nombre = request.GET.get('nombre', '')
    marca_id = request.GET.get('marca_id', '')  # Cambiado a marca_id para usar IDs
    categoria_id = request.GET.get('categoria_id', '')  # Cambiado a categoria_id
    qr_code = request.GET.get('qr_code', '')
    
    # Crear filtros dinámicos
    filtros = Q()
    if nombre:
        filtros &= Q(nombre_producto__icontains=nombre)
    if marca_id:
        filtros &= Q(marca_id=marca_id)
    if categoria_id:
        filtros &= Q(categoria_id=categoria_id)
    if qr_code:
        filtros &= Q(qr_code__icontains=qr_code)
    
    # Aplicar filtros
    if filtros != Q():
        productos_list = productos_list.filter(filtros)
    
    # Paginación
    paginator = Paginator(productos_list, 6)
    page = request.GET.get('page', 1)
    
    try:
        productos = paginator.get_page(page)
    except:
        productos = paginator.get_page(1)
    
    # Obtener todas las marcas para el selector principal
    marcas = Marca.objects.all().order_by('nombre_marca')
    
    # Obtener categorías según la marca seleccionada
    if marca_id:
        # Si hay marca seleccionada, mostrar solo categorías relacionadas con productos de esa marca
        categorias = Categoria.objects.filter(
            producto__marca_id=marca_id
        ).distinct().order_by('nombre_categoria')
        
        # Obtener la marca seleccionada para mostrarla en el filtro
        marca_seleccionada = Marca.objects.get(id=marca_id)
        marca_nombre = marca_seleccionada.nombre_marca
    else:
        # Si no hay marca seleccionada, mostrar todas las categorías
        categorias = Categoria.objects.all().order_by('nombre_categoria')
        marca_nombre = ""
    
    # Obtener la categoría seleccionada si existe
    categoria_nombre = ""
    if categoria_id:
        try:
            categoria_seleccionada = Categoria.objects.get(id=categoria_id)
            categoria_nombre = categoria_seleccionada.nombre_categoria
        except Categoria.DoesNotExist:
            pass
    
    # Contexto para la plantilla
    context = {
        'productos': productos,
        'nombre': nombre,
        'marca_id': marca_id,
        'marca_nombre': marca_nombre,
        'categoria_id': categoria_id,
        'categoria_nombre': categoria_nombre,
        'qr_code': qr_code,
        'marcas': marcas,
        'categorias': categorias,
    }
    
    return render(request, 'mi_app/producto/listar.html', context)

# Nueva vista para obtener categorías por AJAX
def get_categorias_por_marca(request):
    marca_id = request.GET.get('marca_id', '')
    
    if not marca_id:
        return JsonResponse({'error': 'No se proporcionó ID de marca'}, status=400)
    
    try:
        # Obtener categorías relacionadas con productos de esta marca
        categorias = Categoria.objects.filter(
            producto__marca_id=marca_id
        ).distinct().values('id', 'nombre_categoria').order_by('nombre_categoria')
        
        return JsonResponse({'categorias': list(categorias)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductoForm
from .models import Producto

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            
            # Mostrar mensaje de advertencia si hay alguno
            if hasattr(form, 'add_warning') and form.add_warning:
                messages.warning(request, form.add_warning)
                
            messages.success(request, f"Producto '{producto.nombre_producto}' creado correctamente.")
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'mi_app/producto/crear_editar_producto.html', {'form': form})

def editar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            
            # Mostrar mensaje de advertencia si hay alguno
            if hasattr(form, 'add_warning') and form.add_warning:
                messages.warning(request, form.add_warning)
                
            messages.success(request, f"Producto '{producto.nombre_producto}' actualizado correctamente.")
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'mi_app/producto/crear_editar_producto.html', {'form': form})

# Eliminar Producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('listar_productos')
    return render(request, 'mi_app/producto/confirmar_eliminar.html', {'producto': producto})

## mas funcionalidaddes producto
from decimal import Decimal

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    # Realizamos el cálculo del precio sin IVA
    precio_sin_iva = producto.precio / Decimal('1.18')  # Convertir el 1.18 a Decimal

    # Consultamos el tipo de motor
    tipo_motor = producto.tipo_motor

    # Contexto a pasar a la plantilla
    context = {
        'producto': producto,
        'precio_sin_iva': precio_sin_iva,
        'tipo_motor': tipo_motor,
    }

    return render(request, 'mi_app/producto/detalle.html', context)





#3♣3♣35#3♣3♣35353535#                                      tipo producto

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TipoProducto
from .forms import TipoProductoForm

# Vista para listar todos los tipos de productos
def tipo_producto_list(request):
    tipo_productos = TipoProducto.objects.all()
    return render(request, 'mi_app/tipo_producto/tipo_producto_list.html', {'tipo_productos': tipo_productos})

# Vista para crear un nuevo tipo de producto
def tipo_producto_create(request):
    if request.method == 'POST':
        form = TipoProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipo_productos_listar')  # Redirección a la vista de listar productos
    else:
        form = TipoProductoForm()
    return render(request, 'mi_app/tipo_producto/tipo_producto_form.html', {'form': form})

# Vista para editar un tipo de producto existente
def tipo_producto_edit(request, pk):
    tipo_producto = get_object_or_404(TipoProducto, pk=pk)
    if request.method == 'POST':
        form = TipoProductoForm(request.POST, instance=tipo_producto)
        if form.is_valid():
            form.save()
            return redirect('tipo_productos_listar')  # Redirección a la vista de listar productos
    else:
        form = TipoProductoForm(instance=tipo_producto)
    return render(request, 'mi_app/tipo_producto/tipo_producto_form.html', {'form': form})

# Vista para eliminar un tipo de producto
def tipo_producto_delete(request, pk):
    tipo_producto = get_object_or_404(TipoProducto, pk=pk)
    if request.method == 'POST':
        tipo_producto.delete()
        return redirect('tipo_productos_listar')  # Redirección a la vista de listar productos
    return render(request, 'mi_app/tipo_producto/tipo_producto_confirm_delete.html', {'tipo_producto': tipo_producto})


#3♣3♣35#3♣3♣35353535#                                      producto tipo


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import ProductoTipo, Producto, TipoProducto
from .forms import ProductoTipoForm

# Vista para listar todas las relaciones Producto-TipoProducto
def producto_tipo_list(request):
    producto_tipos = ProductoTipo.objects.all()
    return render(request, 'mi_app/producto_tipo/tipo_producto_list.html', {'producto_tipos': producto_tipos})

# Vista para crear una nueva relación entre Producto y TipoProducto
def producto_tipo_create(request):
    if request.method == 'POST':
        form = ProductoTipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La relación Producto-TipoProducto se ha creado correctamente.')
            return redirect('producto_tipo_list')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ProductoTipoForm()

    return render(request, 'mi_app/producto_tipo/tipo_producto_form.html', {'form': form})

# Vista para editar una relación Producto-TipoProducto existente
def producto_tipo_edit(request, pk):
    producto_tipo = get_object_or_404(ProductoTipo, pk=pk)
    if request.method == 'POST':
        form = ProductoTipoForm(request.POST, instance=producto_tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'La relación Producto-TipoProducto se ha actualizado correctamente.')
            return redirect('producto_tipo_list')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ProductoTipoForm(instance=producto_tipo)
    
    return render(request, 'mi_app/producto_tipo/tipo_producto_form.html', {'form': form})

# Vista para eliminar una relación Producto-TipoProducto
def producto_tipo_delete(request, pk):
    producto_tipo = get_object_or_404(ProductoTipo, pk=pk)
    if request.method == 'POST':
        producto_tipo.delete()
        messages.success(request, 'La relación Producto-TipoProducto ha sido eliminada correctamente.')
        return redirect('producto_tipo_list')
    return render(request, 'mi_app/producto_tipo/tipo_producto_confirm_delete.html', {'producto_tipo': producto_tipo})


#3♣3♣35#3♣3♣35353535#                                      clientes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm

import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm

API_URL = "https://apiperu.dev/api/dni"
API_TOKEN = "379335fdc99791867e0a7a40cd82c289afd112ed61daf7d4cf9ac325b9033f2f"

# Listar clientes
from django.core.paginator import Paginator
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from .models import Cliente

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from .models import Cliente

def lista_clientes(request):
    query = request.GET.get("q", "").strip()  # Obtener y limpiar el término de búsqueda
    ordenar_por = request.GET.get("orden", "fecha_registro")  # Obtener el criterio de orden

    # Asegurar que ordenar_por sea un campo válido para evitar errores
    campos_validos = ["nombre_cliente", "fecha_registro", "dni"]
    if ordenar_por not in campos_validos:
        ordenar_por = "fecha_registro"

    clientes = Cliente.objects.all()

    # Filtro de búsqueda
    if query:
        clientes = clientes.filter(
            Q(dni__icontains=query) |
            Q(nombre_cliente__icontains=query)
        )

    # Ordenación segura
    clientes = clientes.order_by(ordenar_por)

    # Paginación (5 clientes por página)
    paginator = Paginator(clientes, 5)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Si no es un número, ir a la primera página
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Si está fuera de rango, ir a la última página

    return render(request, "mi_app/clientes/listar_clientes.html", {
        "clientes": page_obj,
        "query": query,
        "ordenar_por": ordenar_por
    })



# Buscar DNI y guardar en la BD
def buscar_dni(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]

            # Verificar si el cliente ya existe
            if Cliente.objects.filter(dni=dni).exists():
                messages.warning(request, "El cliente ya está registrado.")
                return redirect("lista_clientes")

            # Consultar la API
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_TOKEN}",
            }
            response = requests.post(API_URL, json={"dni": dni}, headers=headers)

            if response.status_code == 200:
                resultado = response.json()
                if resultado.get("success"):
                    datos = resultado["data"]

                    # Guardar cliente en la BD
                    Cliente.objects.create(
                        dni=datos["numero"],
                        nombre_cliente=datos["nombres"],
                        apellido_paterno=datos["apellido_paterno"],
                        apellido_materno=datos["apellido_materno"],
                        direccion_cliente=datos.get("direccion", "")
                    )

                    messages.success(request, "Cliente registrado exitosamente.")
                    return redirect("lista_clientes")
                else:
                    messages.error(request, "No se encontró información para el DNI ingresado.")
            else:
                messages.error(request, "Error al conectar con la API.")
    else:
        form = ClienteForm()

    return render(request, "mi_app/clientes/buscar_dni.html", {"form": form})

# Editar cliente
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("lista_clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "mi_app/clientes/editar_cliente.html", {"form": form, "cliente": cliente})

# Eliminar cliente
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect("lista_clientes")


from django.http import JsonResponse

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    data = {
        "dni": cliente.dni,
        "nombre": cliente.nombre_cliente,
        "apellido_paterno": cliente.apellido_paterno,
        "apellido_materno": cliente.apellido_materno,
        "telefono": cliente.telefono_cliente,
        "email": cliente.email_cliente,
        "direccion": cliente.direccion_cliente,
        "fecha_registro": cliente.fecha_registro.strftime("%d-%m-%Y %H:%M"),
    }
    return JsonResponse(data)
### -------------------------------------------------------Clientes Version 2
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Cliente
from .forms import ClientesForm

class ClientesListView(ListView):
    model = Cliente
    template_name = 'mi_app/clientesv1/clientes_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        """
        Permite búsqueda por DNI, nombre, apellido o correo
        """
        query = self.request.GET.get('q', '')
        if query:
            return Cliente.objects.filter(
                Q(dni__icontains=query) | 
                Q(nombre_cliente__icontains=query) | 
                Q(apellido_paterno__icontains=query) | 
                Q(apellido_materno__icontains=query) | 
                Q(email_cliente__icontains=query)
            )
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        """
        Añade parámetro de búsqueda al contexto
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class ClientesCreateView(CreateView):
    model = Cliente
    form_class = ClientesForm
    template_name = 'mi_app/clientesv1/clientes_form.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        """
        Añade mensaje de éxito cuando el formulario es válido
        """
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Añade mensaje de error cuando el formulario no es válido
        """
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

class ClientesUpdateView(UpdateView):
    model = Cliente
    form_class = ClientesForm
    template_name = 'mi_app/clientesv1/clientes_form.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        """
        Añade mensaje de éxito cuando el formulario es válido
        """
        messages.success(self.request, 'Cliente actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Añade mensaje de error cuando el formulario no es válido
        """
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Añade una bandera para indicar que es una edición
        """
        context = super().get_context_data(**kwargs)
        context['es_edicion'] = True
        return context

class ClientesDeleteView(DeleteView):
    model = Cliente
    template_name = 'mi_app/clientesv1/clientes_confirm_delete.html'
    success_url = reverse_lazy('clientes:lista')

    def delete(self, request, *args, **kwargs):
        """
        Añade mensaje de éxito al eliminar
        """
        messages.success(request, 'Cliente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

def cliente_detalle(request, pk):
    """
    Vista para mostrar detalles de un cliente
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'mi_app/clientesv1/clientes_detalle.html', {'cliente': cliente})







#3♣3♣35#3♣3♣35353535#                                      proveedores

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Proveedor
from .forms import ProveedorForm

# Vista para listar los proveedores
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'mi_app/proveedores/listar_proveedores.html', {'proveedores': proveedores})

# Vista para crear un nuevo proveedor
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado con éxito')
            return redirect('listar_proveedores')
        else:
            messages.error(request, 'Hubo un error al crear el proveedor')
    else:
        form = ProveedorForm()
    
    return render(request, 'mi_app/proveedores/crear_proveedor.html', {'form': form})

# Vista para editar un proveedor existente
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado con éxito')
            return redirect('listar_proveedores')
        else:
            messages.error(request, 'Hubo un error al actualizar el proveedor')
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'mi_app/proveedores/editar_proveedor.html', {'form': form, 'proveedor': proveedor})

# Vista para eliminar un proveedor
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado con éxito')
        return redirect('listar_proveedores')
    
    return render(request, 'mi_app/proveedores/eliminar_proveedor.html', {'proveedor': proveedor})


#3♣3♣35#3♣3♣35353535#                                      Compra
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Compra
from .forms import CompraForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Compra
from .forms import CompraForm

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Compra

def listar_compras(request):
    compras = Compra.objects.all()

    # Filtrado por fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        compras = compras.filter(fecha_compra__date__range=[fecha_inicio, fecha_fin])

    # Paginación
    paginator = Paginator(compras, 10)  # 10 compras por página
    page = request.GET.get('page')
    compras_paginadas = paginator.get_page(page)

    return render(request, 'mi_app/compras/listar_compras.html', {
        'compras': compras_paginadas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })

# Vista para crear una nueva compra
def crear_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST, request.FILES)  # Manejo de archivos con request.FILES
        if form.is_valid():
            compra = form.save()
            if compra.total_compra == 0:
                messages.warning(request, 'Compra registrada con total de 0 soles.')
            else:
                messages.success(request, 'Compra creada con éxito')
            return redirect('listar_compras')
        else:
            messages.error(request, 'Hubo un error al crear la compra')
    else:
        form = CompraForm(initial={'fecha_compra': None})  # Permitir que el usuario seleccione la fecha
    
    return render(request, 'mi_app/compras/crear_compra.html', {'form': form})

# Vista para editar una compra
def editar_compra(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    
    if request.method == 'POST':
        form = CompraForm(request.POST, request.FILES, instance=compra)  # Manejo de archivos con request.FILES
        if form.is_valid():
            compra = form.save()
            if compra.total_compra == 0:
                messages.warning(request, 'Compra actualizada con total de 0 soles.')
            else:
                messages.success(request, 'Compra actualizada con éxito')
            return redirect('listar_compras')
        else:
            messages.error(request, 'Hubo un error al actualizar la compra')
    else:
        form = CompraForm(instance=compra)  # Crear el formulario con los datos de la compra
    
    return render(request, 'mi_app/compras/editar_compra.html', {'form': form, 'compra': compra})

# Vista para eliminar una compra
def eliminar_compra(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminada con éxito')
        return redirect('listar_compras')
    
    return render(request, 'mi_app/compras/eliminar_compra.html', {'compra': compra})



#3♣3♣35#3♣3♣35353535#                                      Detalle de comprea


from django.shortcuts import render, get_object_or_404
from .models import Compra, DetalleCompra
from .forms import DetalleCompraForm
from django.contrib import messages
from django.shortcuts import redirect

# Vista para listar los detalles de la compra
def listar_detalles(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    detalles = DetalleCompra.objects.filter(compra=compra)
    return render(request, 'mi_app/decompras/listar_detalles.html', {'compra': compra, 'detalles': detalles})


def agregar_detalle(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    
    if request.method == 'POST':
        form = DetalleCompraForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.compra = compra  # Asociamos el detalle con la compra
            detalle.save()
            messages.success(request, 'Detalle de compra agregado con éxito')
            return redirect('listar_detalles', compra_id=compra.id)
        else:
            messages.error(request, 'Hubo un error al agregar el detalle')
    else:
        form = DetalleCompraForm()

    return render(request, 'mi_app/decompras/agregar_detalle.html', {'form': form, 'compra': compra})


def editar_detalle(request, compra_id, detalle_id):
    detalle = get_object_or_404(DetalleCompra, pk=detalle_id, compra__id=compra_id)
    
    if request.method == 'POST':
        form = DetalleCompraForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Detalle de compra actualizado con éxito')
            return redirect('listar_detalles', compra_id=compra_id)
        else:
            messages.error(request, 'Hubo un error al actualizar el detalle')
    else:
        form = DetalleCompraForm(instance=detalle)

    return render(request, 'mi_app/decompras/editar_detalle.html', {'form': form, 'compra': detalle.compra, 'detalle': detalle})

def eliminar_detalle(request, compra_id, detalle_id):
    detalle = get_object_or_404(DetalleCompra, pk=detalle_id, compra__id=compra_id)
    
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Detalle de compra eliminado con éxito')
        return redirect('listar_detalles', compra_id=compra_id)
    
    return render(request, 'mi_app/decompras/eliminar_detalle.html', {'detalle': detalle})



#                                                      ventas
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm

# Vista para listar ventas
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Venta, DetalleVenta

# Vista mejorada para listar ventas
def listar_ventas(request):
    # Obtener todos los registros de ventas ordenados por fecha (más recientes primero)
    ventas_list = Venta.objects.all().order_by('-fecha_venta')
    
    # Filtros de búsqueda
    search_query = request.GET.get('search', '')
    date_filter = request.GET.get('date_filter', '')
    sort_by = request.GET.get('sort', 'date-desc')
    
    # Aplicar filtro de búsqueda si existe
    if search_query:
        ventas_list = ventas_list.filter(
            numero_documento__icontains=search_query
        ) | ventas_list.filter(
            cliente_nombre__icontains=search_query
        )
    
    # Aplicar filtro de fecha
    today = timezone.now().date()
    if date_filter == 'today':
        ventas_list = ventas_list.filter(fecha_venta__date=today)
    elif date_filter == 'week':
        start_of_week = today - timedelta(days=today.weekday())
        ventas_list = ventas_list.filter(fecha_venta__date__gte=start_of_week)
    elif date_filter == 'month':
        ventas_list = ventas_list.filter(
            fecha_venta__year=today.year,
            fecha_venta__month=today.month
        )
    
    # Aplicar ordenamiento
    if sort_by == 'date-asc':
        ventas_list = ventas_list.order_by('fecha_venta')
    elif sort_by == 'amount-desc':
        ventas_list = ventas_list.order_by('-total_venta')
    elif sort_by == 'amount-asc':
        ventas_list = ventas_list.order_by('total_venta')
    # Por defecto: date-desc, ya aplicado inicialmente
    
    # Paginación (10 ventas por página)
    paginator = Paginator(ventas_list, 10)
    page = request.GET.get('page')
    ventas = paginator.get_page(page)
    
    # Estadísticas
    # Total de ventas del día
    ventas_hoy = Venta.objects.filter(fecha_venta__date=today).count()
    
    # Total de ventas en general
    total_ventas = Venta.objects.count()
    
    # Monto total de todas las ventas
    monto_total = Venta.objects.aggregate(total=Sum('total_venta'))['total'] or 0
    
    # Contexto con toda la información
    context = {
        'ventas': ventas,
        'total_ventas': total_ventas,
        'ventas_hoy': ventas_hoy,
        'monto_total': monto_total,
        'search_query': search_query,
        'date_filter': date_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'mi_app/ventas/listar_ventas.html', context)

# Crear nueva venta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max
from .models import Venta, Cliente, TipoDocumento
from .forms import VentaForm
# from .utils import generar_numero_documento

# Vista mejorada para crear venta
def crear_venta(request):
    # Obtener clientes recientes para acceso rápido
    clientes_recientes = Cliente.objects.all().order_by('-fecha_registro')[:5]
    
    # Generar automáticamente el próximo número de documento
    ultimo_numero = Venta.objects.aggregate(Max('numero_documento'))['numero_documento__max'] or '000000'
    
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            nueva_venta = form.save(commit=False)
            
            # Verificar y generar número de documento si está vacío
            if not nueva_venta.numero_documento:
                tipo_doc = nueva_venta.tipo_documento.tipo_documento
                nueva_venta.numero_documento = generar_numero_documento(tipo_doc)
            
            # Agregar fecha actual
            nueva_venta.fecha_venta = timezone.now()
            
            # Guardar la venta
            nueva_venta.save()
            
            messages.success(request, f'Venta {nueva_venta.numero_documento} registrada con éxito')
            
            # Redireccionar a agregar detalles de venta directamente
            return redirect('agregar_detalle_venta', venta_id=nueva_venta.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
    else:
        # Inicializar formulario
        form = VentaForm(initial={
            'numero_documento': str(int(ultimo_numero) + 1).zfill(6),
            'total_venta': 0
        })
    
    # Obtener últimas ventas para referencia
    ultimas_ventas = Venta.objects.all().order_by('-fecha_venta')[:3]
    
    context = {
        'form': form,
        'clientes_recientes': clientes_recientes,
        'ultimas_ventas': ultimas_ventas,
        'titulo_pagina': 'Registrar Nueva Venta',
    }
    
    return render(request, 'mi_app/ventas/crear_venta.html', context)

# Editar venta
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venta actualizada correctamente')
            return redirect('listar_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'mi_app/ventas/editar_venta.html', {'form': form, 'venta': venta})

# Eliminar venta
def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente')
        return redirect('listar_ventas')
    return render(request, 'mi_app/ventas/eliminar_venta.html', {'venta': venta})


# Importar las librerías necesarias para AJAX
from django.http import JsonResponse
from django.db.models import Q
from .models import Cliente

# Vista para búsqueda de clientes con AJAX
def buscar_clientes_ajax(request):
    """
    Vista para buscar clientes mediante AJAX para Select2
    """
    search = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    # Limitar resultados a 10 por página para mejor rendimiento
    offset = (page - 1) * 10
    limit = page * 10
    
    # Buscar clientes que coincidan con el término de búsqueda
    if search:
        # Buscar en nombre, apellidos, DNI o RUC
        clientes = Cliente.objects.filter(
            Q(nombre_cliente__icontains=search) | 
            Q(apellido_paterno__icontains=search) | 
            Q(apellido_materno__icontains=search) | 
            Q(dni__icontains=search) | 
            Q(ruc_cliente__icontains=search)
        ).order_by('nombre_cliente')
    else:
        # Si no hay término de búsqueda, mostrar los clientes más recientes
        clientes = Cliente.objects.all().order_by('-fecha_registro')
    
    # Contar total de resultados para paginación
    total_count = clientes.count()
    
    # Aplicar paginación
    clientes = clientes[offset:limit]
    
    # Preparar datos para Select2
    results = []
    for cliente in clientes:
        nombre_completo = cliente.nombre_cliente
        if cliente.apellido_paterno:
            nombre_completo += f" {cliente.apellido_paterno}"
        if cliente.apellido_materno:
            nombre_completo += f" {cliente.apellido_materno}"
            
        results.append({
            'id': cliente.id,
            'text': f"{nombre_completo} - {cliente.dni}",
            # Datos adicionales que usaremos con JavaScript
            'nombre_cliente': nombre_completo,
            'dni': cliente.dni,
            'telefono': cliente.telefono_cliente or '',
            'email': cliente.email_cliente or '',
            'direccion': cliente.direccion_cliente or '',
            'ruc': cliente.ruc_cliente or ''
        })
    
    # Formato esperado por Select2
    data = {
        'results': results,
        'pagination': {
            'more': total_count > limit
        }
    }
    
    return JsonResponse(data)

# Vista para obtener información detallada de un cliente mediante AJAX
def obtener_info_cliente_ajax(request, cliente_id):
    """
    Vista para obtener información detallada de un cliente mediante AJAX
    """
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
        
        # Construir nombre completo
        nombre_completo = cliente.nombre_cliente
        if cliente.apellido_paterno:
            nombre_completo += f" {cliente.apellido_paterno}"
        if cliente.apellido_materno:
            nombre_completo += f" {cliente.apellido_materno}"
        
        # Preparar datos para respuesta JSON
        data = {
            'success': True,
            'cliente': {
                'id': cliente.id,
                'nombre_cliente': nombre_completo,
                'dni': cliente.dni,
                'telefono': cliente.telefono_cliente or '',
                'email': cliente.email_cliente or '',
                'direccion': cliente.direccion_cliente or '',
                'ruc': cliente.ruc_cliente or '',
                'contacto': cliente.contacto_cliente or cliente.telefono_cliente or cliente.email_cliente or ''
            }
        }
    except Cliente.DoesNotExist:
        data = {
            'success': False,
            'error': 'Cliente no encontrado'
        }
    
    return JsonResponse(data)

#                                                    Detalles Ventas

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DetalleVenta, Venta, Producto
from .forms import DetalleVentaForm

# # Listar detalles de una venta específica
# def listar_detalles_venta(request, venta_id):
#     venta = get_object_or_404(Venta, pk=venta_id)
#     detalles = DetalleVenta.objects.filter(venta=venta)
#     return render(request, 'mi_app/deventas/listar_detalles_venta.html', {'venta': venta, 'detalles': detalles})

# # Agregar nuevo detalle a una venta
# def agregar_detalle_venta(request, venta_id):
#     venta = get_object_or_404(Venta, pk=venta_id)

#     if request.method == 'POST':
#         form = DetalleVentaForm(request.POST)
#         if form.is_valid():
#             detalle = form.save(commit=False)
#             detalle.venta = venta
#             detalle.save()
#             messages.success(request, 'Detalle agregado con éxito.')
#             return redirect('listar_detalles_venta', venta_id=venta.id)
#         else:
#             messages.error(request, 'Hubo un error al agregar el detalle.')
#     else:
#         form = DetalleVentaForm()

#     return render(request, 'mi_app/deventas/agregar_detalle_venta.html', {'form': form, 'venta': venta})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.urls import reverse
import json

from .models import Venta, DetalleVenta, Producto
from .forms import DetalleVentaForm

from .models import Venta, DetalleVenta, Producto
from .forms import DetalleVentaForm

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse


from django.contrib import messages

from django.db import transaction
from django.urls import reverse
from django.db.models import Q
import json
import logging

from .models import Venta, DetalleVenta, Producto
from .forms import DetalleVentaForm, ProductoSearchForm

# Configurar logger
logger = logging.getLogger(__name__)

def buscar_productos_ajax(request):
    """
    Vista mejorada para búsqueda de productos con AJAX para Select2.
    Optimizada para rendimiento y compatibilidad con Select2.   
    """
    search_term = request.GET.get('q', '')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    
    limit = 10
    offset = (page - 1) * limit
    
    # Inicializar la consulta base con las relaciones para optimizar rendimiento
    query = Producto.objects.select_related('marca', 'categoria', 'tipo_motor')
    
    # Aplicar filtros de búsqueda si hay término
    if search_term and len(search_term) >= 1:
        query = query.filter(
            Q(nombre_producto__icontains=search_term) |
            Q(marca__nombre__icontains=search_term) |
            Q(categoria__nombre__icontains=search_term)
        )
    
    # Filtrar por stock disponible (opcional, comentar si se necesitan ver todos)
    query = query.filter(stock__gt=0)
    
    # Contar total para paginación (solo una vez)
    total_count = query.count()
    has_more = total_count > offset + limit
    
    # Obtener los productos paginados
    productos = query[offset:offset + limit]
    
    # Preparar los resultados en formato compatible con Select2
    results = []
    for p in productos:
        try:
            results.append({
                'id': p.id,
                'text': p.nombre_producto,  # Importante: Select2 requiere 'text'
                'nombre': p.nombre_producto,
                'marca': getattr(p.marca, 'nombre', "Sin marca"),
                'categoria': getattr(p.categoria, 'nombre', "Sin categoría"),
                'tipo_motor': getattr(p.tipo_motor, 'nombre', "Sin tipo"),
                'stock': p.stock,
                'precio': float(p.precio)
            })
        except Exception as e:
            logger.error(f"Error procesando producto {p.id}: {str(e)}")
    
    # Retornar respuesta JSON en formato esperado por Select2
    return JsonResponse({
        'results': results,
        'pagination': {
            'more': has_more
        }
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.urls import reverse

from .models import Venta, DetalleVenta, Producto
from .forms import DetalleVentaForm



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
import logging

from .models import Venta, DetalleVenta, Producto
from .forms import ProductoSearchForm, AgregarProductoForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
import logging
from .models import Venta, Producto, DetalleVenta
from .forms import ProductoSearchForm, AgregarProductoForm, EliminarProductoForm, FinalizarVentaForm

# Configurar logger
logger = logging.getLogger(__name__)

def agregar_detalle_venta(request, venta_id):
    """
    Vista completa para agregar productos a una venta sin AJAX.
    Utiliza formularios tradicionales y sesiones para mantener el carrito.
    """
    # Obtener la venta o devolver un 404 si no existe
    venta = get_object_or_404(Venta, pk=venta_id)
    
    # Inicializar el carrito en la sesión si no existe
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    
    # Procesar formulario de búsqueda
    search_form = ProductoSearchForm(request.GET)
    productos = None
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('q', '')
        if query:
            # Buscar productos por nombre, marca o categoría
            productos = Producto.objects.select_related('marca', 'categoria', 'tipo_motor').filter(
                Q(nombre_producto__icontains=query) |
                Q(marca__nombre_marca__icontains=query) |
                Q(categoria__nombre_categoria__icontains=query)
            ).order_by('nombre_producto')[:30]  # Limitar a 30 resultados
            
            logger.info(f"Búsqueda de productos con término '{query}': {productos.count()} resultados")
    
    # Procesar solicitudes POST
    if request.method == 'POST':
        # 1. Agregar producto al carrito
        if 'agregar_producto' in request.POST:
            agregar_form = AgregarProductoForm(request.POST)
            
            if agregar_form.is_valid():
                producto_id = agregar_form.cleaned_data['producto_id']
                cantidad = agregar_form.cleaned_data['cantidad']
                precio_unitario = agregar_form.cleaned_data['precio_unitario']
                
                try:
                    # Obtener el producto y validar su existencia
                    producto = get_object_or_404(Producto, pk=producto_id)
                    
                    # Validar stock disponible
                    if cantidad > producto.stock:
                        messages.error(request, f"Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.stock}")
                        return redirect(request.get_full_path())
                    
                    # Calcular subtotal
                    subtotal = cantidad * precio_unitario
                    
                    # Agregar al carrito en la sesión
                    carrito = request.session['carrito']
                    carrito.append({
                        'producto_id': producto.id,
                        'nombre': producto.nombre_producto,
                        'marca': producto.marca.nombre_marca if producto.marca else "Sin marca",
                        'categoria': producto.categoria.nombre_categoria if producto.categoria else "Sin categoría",
                        'tipo_motor': producto.tipo_motor.tipo_motor if producto.tipo_motor else "Sin tipo",
                        'cantidad': cantidad,
                        'precio': str(precio_unitario),  # Convertir a string para serialización JSON
                        'subtotal': str(subtotal)
                    })
                    
                    request.session['carrito'] = carrito
                    request.session.modified = True
                    
                    messages.success(request, f"{producto.nombre_producto} agregado a la venta")
                    logger.info(f"Producto {producto.id} agregado al carrito para venta {venta_id}")
                    
                except Producto.DoesNotExist:
                    messages.error(request, "El producto seleccionado no existe")
                    logger.warning(f"Intento de agregar producto inexistente ID={producto_id}")
                except Exception as e:
                    messages.error(request, f"Error al agregar producto: {str(e)}")
                    logger.error(f"Error al agregar producto: {str(e)}", exc_info=True)
            else:
                # Mostrar errores de validación del formulario
                for field, errors in agregar_form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en {field}: {error}")
            
            # Redireccionar para evitar reenvío del formulario
            return redirect(request.get_full_path())
        
        # 2. Eliminar producto del carrito
        elif 'eliminar_producto' in request.POST:
            try:
                producto_index = int(request.POST.get('producto_index', -1))
                carrito = request.session.get('carrito', [])
                
                if 0 <= producto_index < len(carrito):
                    # Guardar información para mensaje
                    producto_eliminado = carrito[producto_index]['nombre']
                    
                    # Eliminar del carrito
                    del carrito[producto_index]
                    request.session['carrito'] = carrito
                    request.session.modified = True
                    
                    messages.warning(request, f"Producto '{producto_eliminado}' eliminado de la venta")
                    logger.info(f"Producto eliminado del carrito en posición {producto_index}")
                else:
                    messages.error(request, "Índice de producto inválido")
            except Exception as e:
                messages.error(request, f"Error al eliminar producto: {str(e)}")
                logger.error(f"Error al eliminar producto: {str(e)}", exc_info=True)
            
            # Redireccionar para evitar reenvío del formulario
            return redirect(request.get_full_path())
        
        # 3. Finalizar venta
        elif 'finalizar_venta' in request.POST:
            carrito = request.session.get('carrito', [])
            
            # Validar que haya productos en el carrito
            if not carrito:
                messages.error(request, "No hay productos en la venta")
                return redirect(request.get_full_path())
            
            try:
                # Usar transacción para asegurar integridad de los datos
                with transaction.atomic():
                    # Calcular total de la venta
                    total_venta = sum(float(item['subtotal']) for item in carrito)
                    
                    # Actualizar el total de la venta
                    venta.total_venta = total_venta
                    venta.save()
                    
                    logger.info(f"Actualizando venta {venta.id} con total {total_venta}")
                    
                    # Crear detalles de venta y actualizar inventario
                    for item in carrito:
                        producto = get_object_or_404(Producto, pk=item['producto_id'])
                        cantidad = int(item['cantidad'])
                        precio_unitario = float(item['precio'])
                        
                        # Verificar stock nuevamente (podría haber cambiado)
                        if cantidad > producto.stock:
                            raise ValueError(f"Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.stock}")
                        
                        # Crear detalle de venta
                        detalle = DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=cantidad * precio_unitario
                        )
                        
                        logger.info(f"Detalle creado: ID={detalle.id}, Producto={producto.id}, Cantidad={cantidad}")
                        
                        # Actualizar stock del producto
                        producto.stock -= cantidad
                        producto.save()
                        
                        logger.info(f"Stock actualizado para producto {producto.id}. Nuevo stock: {producto.stock}")
                    
                    # Limpiar carrito
                    request.session['carrito'] = []
                    request.session.modified = True
                    
                    messages.success(request, "Venta finalizada correctamente")
                    logger.info(f"Venta {venta.id} finalizada exitosamente")
                    
                    # Redireccionar a la lista de detalles
                    return redirect('listar_detalles_venta', venta_id=venta.id)
                    
            except ValueError as e:
                messages.error(request, str(e))
                logger.warning(f"Error de validación al finalizar venta: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error al finalizar venta: {str(e)}")
                logger.error(f"Error al finalizar venta {venta.id}: {str(e)}", exc_info=True)
            
            # En caso de error, redireccionar a la misma página
            return redirect(request.get_full_path())
    
    # Calcular total del carrito para mostrar en la página
    carrito = request.session.get('carrito', [])
    total_carrito = sum(float(item['subtotal']) for item in carrito)
    
    # Obtener detalles existentes para referencia (opcional)
    detalles_existentes = DetalleVenta.objects.filter(venta=venta).select_related('producto')
    
    # Contexto para la plantilla
    context = {
        'venta': venta,
        'search_form': search_form,
        'productos': productos,
        'carrito': carrito,
        'total_carrito': total_carrito,
        'detalles_existentes': detalles_existentes
    }
    
    # Renderizar plantilla
    return render(request, 'mi_app/deventas/agregar_detalle_venta.html', context)


def listar_detalles_venta(request, venta_id):
    """
    Vista para mostrar todos los detalles de una venta.
    """
    venta = get_object_or_404(Venta, pk=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta).select_related('producto')
    
    return render(request, 'mi_app/deventas/listar_detalles_venta.html', {
        'venta': venta,
        'detalles': detalles
    })

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Venta, DetalleVenta

def imprimir_venta_html(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta).select_related('producto')
    
    context = {
        'venta': venta,
        'detalles': detalles,
        'fecha_actual': datetime.now(),
        'imprimir': True,  # Para indicar que es vista de impresión
    }
    
    return render(request, 'mi_app/deventas/imprimir_venta.html', context)

# Editar detalle de una venta
def editar_detalle_venta(request, detalle_id):
    """
    Vista para editar un detalle de venta existente.
    Permite modificar la cantidad y precio unitario.
    """
    detalle = get_object_or_404(DetalleVenta, pk=detalle_id)
    venta = detalle.venta
    producto = detalle.producto
    
    # Guardar valores originales para comparar cambios
    cantidad_original = detalle.cantidad
    precio_original = detalle.precio_unitario
    
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST, instance=detalle)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtener nuevos valores
                    nueva_cantidad = form.cleaned_data['cantidad']
                    nuevo_precio = form.cleaned_data['precio_unitario']
                    
                    # Calcular diferencia de cantidad para actualizar stock
                    diferencia_cantidad = cantidad_original - nueva_cantidad
                    
                    # Actualizar stock del producto
                    if diferencia_cantidad != 0:
                        # Si reducimos cantidad (diferencia positiva), aumentamos stock
                        # Si aumentamos cantidad (diferencia negativa), reducimos stock
                        producto.stock += diferencia_cantidad
                        
                        # Verificar que hay suficiente stock si estamos aumentando la cantidad
                        if diferencia_cantidad < 0 and producto.stock < 0:
                            messages.error(request, f"No hay suficiente stock para {producto.nombre_producto}. Disponible: {producto.stock + abs(diferencia_cantidad)}")
                            return redirect('editar_detalle_venta', detalle_id=detalle.id)
                        
                        producto.save()
                    
                    # Guardar detalle con nuevos valores
                    detalle = form.save(commit=False)
                    detalle.subtotal = nueva_cantidad * nuevo_precio
                    detalle.save()
                    
                    # Recalcular total de la venta
                    venta.total_venta = DetalleVenta.objects.filter(venta=venta).aggregate(
                        total=Sum('subtotal'))['total'] or 0
                    venta.save()
                    
                    messages.success(request, f"Detalle de venta actualizado correctamente")
                    return redirect('listar_detalles_venta', venta_id=venta.id)
            
            except Exception as e:
                messages.error(request, f"Error al actualizar detalle: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = DetalleVentaForm(instance=detalle)
    
    context = {
        'form': form,
        'detalle': detalle,
        'venta': venta,
        'producto': producto
    }
    
    return render(request, 'mi_app/deventas/editar_detalle_venta.html', context)

# Eliminar detalle de una venta
# En views.py
def eliminar_detalle_venta(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, pk=detalle_id)
    venta = detalle.venta
    producto = detalle.producto
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Devolver el stock al producto
                producto.stock += detalle.cantidad
                producto.save()
                
                # Restar el subtotal del total de la venta
                venta.total_venta -= detalle.subtotal
                venta.save()
                
                # Eliminar el detalle
                detalle.delete()
                
                messages.success(request, f"Producto eliminado de la venta correctamente")
        except Exception as e:
            messages.error(request, f"Error al eliminar producto: {str(e)}")
    
    return redirect('listar_detalles_venta', venta_id=venta.id)

# En urls.py
# path('detalles/eliminar/<int:detalle_id>/', views.eliminar_detalle_venta, name='eliminar_detalle_venta'),


##3♣                                               Tipo de  documento

from django.shortcuts import render, get_object_or_404, redirect
from .models import TipoDocumento
from .forms import TipoDocumentoForm

# Listar Tipos de Documento
def listar_tipos_documento(request):
    tipos_documento = TipoDocumento.objects.all()
    return render(request, 'mi_app/tipodocumento/listar_tipos_documento.html', {'tipos_documento': tipos_documento})

# Crear Nuevo Tipo de Documento
def crear_tipo_documento(request):
    if request.method == 'POST':
        form = TipoDocumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos_documento')
    else:
        form = TipoDocumentoForm()
    return render(request, 'mi_app/tipodocumento/form_tipo_documento.html', {'form': form})

# Editar Tipo de Documento
def editar_tipo_documento(request, pk):
    tipo_documento = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == 'POST':
        form = TipoDocumentoForm(request.POST, instance=tipo_documento)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos_documento')
    else:
        form = TipoDocumentoForm(instance=tipo_documento)
    return render(request, 'mi_app/tipodocumento/form_tipo_documento.html', {'form': form})

# Eliminar Tipo de Documento
def eliminar_tipo_documento(request, pk):
    tipo_documento = get_object_or_404(TipoDocumento, pk=pk)
    if request.method == 'POST':
        tipo_documento.delete()
        return redirect('listar_tipos_documento')
    return render(request, 'mi_app/tipodocumento/eliminar_tipo_documento.html', {'tipo_documento': tipo_documento})

from .calculadora_views import calculadora  # Importamos la vista

from .dashboards import dashboard_view # Importamos la vista

from  mi_app.Vistas.exportar_excel  import exportar_productos_excel # Importamos la vista


###                                                     Pedidos

###3♣3♣35#3♣3♣35353535#                                      Calculadora

# views.py
from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from decimal import Decimal
from .forms import CalculadoraForm
from .models import Producto

from django.shortcuts import render
from django.views.generic import FormView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .forms import CalculadoraForm, FiltroProductosForm
from .models import Producto

class CalculadoraProductosView(FormView):
    template_name = 'mi_app/producto/calculadora.html'
    form_class = CalculadoraForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Procesar filtros
        filtro_form = FiltroProductosForm(self.request.GET or None)
        context['filtro_form'] = filtro_form
        
        productos = Producto.objects.all().order_by('nombre_producto')
        
        # Aplicar filtros
        if filtro_form.is_valid():
            busqueda = filtro_form.cleaned_data.get('busqueda')
            categoria = filtro_form.cleaned_data.get('categoria')
            marca = filtro_form.cleaned_data.get('marca')
            tipo_motor = filtro_form.cleaned_data.get('tipo_motor')
            precio_min = filtro_form.cleaned_data.get('precio_min')
            precio_max = filtro_form.cleaned_data.get('precio_max')
            
            if busqueda:
                productos = productos.filter(nombre_producto__icontains=busqueda)
            
            if categoria:
                productos = productos.filter(categoria=categoria)
                
            if marca:
                productos = productos.filter(marca=marca)
                
            if tipo_motor:
                productos = productos.filter(tipo_motor=tipo_motor)
                
            if precio_min is not None:
                productos = productos.filter(precio__gte=precio_min)
                
            if precio_max is not None:
                productos = productos.filter(precio__lte=precio_max)
        
        # Paginación
        paginator = Paginator(productos, 12)  # 12 productos por página
        page_number = self.request.GET.get('page', 1)
        productos_page = paginator.get_page(page_number)
        
        # Obtener productos seleccionados
        selected_ids = self.request.session.get('selected_productos', [])
        productos_seleccionados = Producto.objects.filter(id__in=selected_ids)
        total = sum(producto.precio for producto in productos_seleccionados)
        
        context['productos'] = productos_page
        context['productos_seleccionados'] = productos_seleccionados
        context['total'] = total
        
        return context
    
    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')
        
        if accion == 'agregar':
            producto_id = request.POST.get('producto_id')
            selected_ids = request.session.get('selected_productos', [])
            
            if producto_id and int(producto_id) not in selected_ids:
                selected_ids.append(int(producto_id))
                request.session['selected_productos'] = selected_ids
                
        elif accion == 'eliminar':
            producto_id = request.POST.get('producto_id')
            selected_ids = request.session.get('selected_productos', [])
            
            if producto_id and int(producto_id) in selected_ids:
                selected_ids.remove(int(producto_id))
                request.session['selected_productos'] = selected_ids
                
        elif accion == 'limpiar':
            request.session['selected_productos'] = []
        
        # Si es una solicitud AJAX, devuelve JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            productos_seleccionados = Producto.objects.filter(id__in=request.session.get('selected_productos', []))
            total = sum(producto.precio for producto in productos_seleccionados)
            
            return JsonResponse({
                'total': str(total),
                'count': len(productos_seleccionados),
                'productos': [{'id': p.id, 'nombre': p.nombre_producto, 'precio': str(p.precio)} for p in productos_seleccionados]
            })
        
        return self.get(request, *args, **kwargs)