from sympy import Q
from .models import Marca
from django import forms


#### ---------------------------------------MARCAS--------------------------------------- ####

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre_marca']
        widgets = {
            'nombre_marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la marca'}),
        }

    def clean_nombre_marca(self):
        nombre_marca = self.cleaned_data.get('nombre_marca')
        if not nombre_marca:
            raise forms.ValidationError('El nombre de la marca no puede estar vacío.')
        return nombre_marca

#### ---------------------------------------Categorias--------------------------------------- ####

from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']
        labels = {
            'nombre_categoria': 'Nombre de la Categoría'
        }
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría'
            })
        }
#### ---------------------------------------Tipo Motor--------------------------------------- ####

from django import forms
from .models import TipoMotor

class TipoMotorForm(forms.ModelForm):
    class Meta:
        model = TipoMotor
        fields = ['tipo_motor']
        labels = {
            'tipo_motor': 'Tipo de Motor',
        }
        widgets = {
            'tipo_motor': forms.Select(attrs={'class': 'form-control'}),
        }

#### ---------------------------------------Productos--------------------------------------- ####

# from django import forms
# from .models import Producto

# class ProductoForm(forms.ModelForm):
#     class Meta:
#         model = Producto
#         fields = [
#             'nombre_producto',
#             'marca',
#             'categoria',
#             'tipo_motor',
#             'descripcion',
#             'imagen_url',
#             'qr_code',
#             'precio',
#             'stock'
#         ]
#         labels = {
#             'nombre_producto': 'Nombre del Producto',
#             'marca': 'Marca',
#             'categoria': 'Categoría',
#             'tipo_motor': 'Tipo de Motor',
#             'descripcion': 'Descripción',
#             'imagen_url': 'URL de la Imagen',
#             'qr_code': 'Código QR',
#             'precio': 'Precio',
#             'stock': 'Stock'
#         }
#         widgets = {
#             'nombre_producto': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto'}),
#             'marca': forms.Select(attrs={'class': 'form-select'}),
#             'categoria': forms.Select(attrs={'class': 'form-select'}),
#             'tipo_motor': forms.Select(attrs={'class': 'form-select'}),
#             'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describa el producto'}),
#             'imagen_url': forms.URLInput(attrs={'placeholder': 'https://example.com/imagen.jpg'}),
#             'qr_code': forms.TextInput(attrs={'placeholder': 'Código QR (opcional)'}),
#             'precio': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
#             'stock': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Cantidad en stock'})
#         }


from django import forms
from .models import Producto
from django.core.validators import MinValueValidator, URLValidator
from django.utils.safestring import mark_safe

from django import forms
from .models import Producto
from django.core.validators import URLValidator
import requests
from urllib.parse import urlparse

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre_producto',
            'marca',
            'categoria',
            'tipo_motor',
            'descripcion',
            'imagen_url',
            'qr_code',
            'precio',
            'stock'
        ]
        labels = {
            'nombre_producto': 'Nombre del Producto',
            'marca': 'Marca',
            'categoria': 'Categoría',
            'tipo_motor': 'Tipo de Motor',
            'descripcion': 'Descripción',
            'imagen_url': 'URL de la Imagen',
            'qr_code': 'Código QR',
            'precio': 'Precio',
            'stock': 'Stock'
        }
        widgets = {
            'nombre_producto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto',
                'autocomplete': 'off'
            }),
            'marca': forms.Select(attrs={
                'class': 'form-select select2-control',
                'data-placeholder': 'Seleccione una marca'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select select2-control',
                'data-placeholder': 'Seleccione una categoría'
            }),
            'tipo_motor': forms.Select(attrs={
                'class': 'form-select select2-control',
                'data-placeholder': 'Seleccione un tipo de motor'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa el producto detalladamente',
                'maxlength': 500
            }),
            'imagen_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/imagen.jpg',
                'title': 'Ingrese una URL válida de imagen'
            }),
            'qr_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código QR (opcional)'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Cantidad en stock'
            })
        }
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock
    
    def clean_imagen_url(self):
        url = self.cleaned_data.get('imagen_url')
        if not url:
            return url  # Si no hay URL, no realizamos validación
        
        # Validar que la URL sea sintácticamente correcta
        try:
            URLValidator()(url)
        except forms.ValidationError:
            raise forms.ValidationError("La URL no es válida. Asegúrese de incluir http:// o https://")
        
        # Verificar que la URL tenga una extensión de imagen común
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        if not any(path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
            # Si no tiene extensión de imagen, solo mostramos una advertencia pero permitimos guardar
            self.add_warning = "La URL no parece ser una imagen. Por favor verifique que sea correcta."
        
        # Opcional: Intentar verificar si la URL es accesible
        # Este bloque es opcional porque puede ralentizar el formulario
        try:
            response = requests.head(url, timeout=2)
            if response.status_code != 200:
                self.add_warning = "La URL parece no ser accesible. Verifique que sea correcta."
        except:
            # En caso de error, solo añadimos una advertencia
            self.add_warning = "No se pudo verificar si la URL es accesible."
        
        return url
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_warning = None  # Para almacenar advertencias no críticas
#### --------------------------------------- TipoProducto--------------------------------------- ####





from django import forms
from .models import TipoProducto

class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre_tipo_producto']
        widgets = {
            'nombre_tipo_producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del tipo de producto'})
        }


#### --------------------------------------- productos Tipo--------------------------------------- ####

from django import forms
from .models import ProductoTipo, Producto, TipoProducto

class ProductoTipoForm(forms.ModelForm):
    # Selección del Producto con una lista desplegable
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Selecciona el Producto",
        required=True
    )
    
    # Selección del Tipo de Producto con una lista desplegable
    tipo_producto = forms.ModelChoiceField(
        queryset=TipoProducto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Selecciona el Tipo de Producto",
        required=True
    )

    class Meta:
        model = ProductoTipo
        fields = ['producto', 'tipo_producto']
        # Si deseas personalizar los widgets o la presentación de los campos, puedes hacerlo aquí

    def __init__(self, *args, **kwargs):
        super(ProductoTipoForm, self).__init__(*args, **kwargs)
        # Agregar un placeholder y clase CSS adicional para mejorar la apariencia
        self.fields['producto'].widget.attrs.update({'placeholder': 'Selecciona un producto', 'class': 'form-control'})
        self.fields['tipo_producto'].widget.attrs.update({'placeholder': 'Selecciona un tipo de producto', 'class': 'form-control'})

    # Mejorar la experiencia con validaciones si es necesario
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        tipo_producto = cleaned_data.get('tipo_producto')

        if producto == tipo_producto:
            raise forms.ValidationError('El producto y el tipo de producto no pueden ser el mismo.')
        
        return cleaned_data


#### ---------------------------------------Clientes--------------------------------------- ####

from django import forms
from .models import Cliente

from django import forms
from .models import Cliente

from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    dni = forms.CharField(
        max_length=8,
        min_length=8,
        label="DNI",
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'})  # Bloqueado por defecto
    )
    telefono_cliente = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Teléfono'})
    )
    email_cliente = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Email'})
    )
    direccion_cliente = forms.CharField(
        max_length=255,
        required=False,
        label="Dirección",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Dirección'})
    )
    ruc_cliente = forms.CharField(
        max_length=20,
        required=False,  # No es obligatorio
        label="RUC",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese RUC si aplica'})
    )

    class Meta:
        model = Cliente
        fields = ["dni", "telefono_cliente", "email_cliente", "direccion_cliente", "ruc_cliente"]


### ----------------------------------------Clientes version 2----------------------------- ###

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Cliente

class ClientesForm(forms.ModelForm):
    # Validadores personalizados
    dni_validator = RegexValidator(
        regex=r'^\d{8}$', 
        message='El DNI debe contener exactamente 8 dígitos numéricos.'
    )
    telefono_validator = RegexValidator(
        regex=r'^[9]\d{8}$', 
        message='El número de teléfono debe comenzar con 9 y tener 9 dígitos.'
    )

    # Campos personalizados con widgets mejorados
    dni = forms.CharField(
        label='Documento de Identidad',
        validators=[dni_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su DNI',
            'maxlength': 8,
            'minlength': 8
        })
    )

    nombre_cliente = forms.CharField(
        label='Nombres',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese sus nombres',
            'maxlength': 150
        })
    )

    apellido_paterno = forms.CharField(
        label='Apellido Paterno',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su apellido paterno',
            'maxlength': 100
        })
    )

    apellido_materno = forms.CharField(
        label='Apellido Materno',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su apellido materno',
            'maxlength': 100
        })
    )

    email_cliente = forms.EmailField(
        label='Correo Electrónico',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@dominio.com'
        })
    )

    telefono_cliente = forms.CharField(
        label='Teléfono',
        validators=[telefono_validator],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su número de teléfono',
            'maxlength': 9,
            'minlength': 9
        })
    )

    direccion_cliente = forms.CharField(
        label='Dirección',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su dirección',
            'maxlength': 255
        })
    )

    ruc_cliente = forms.CharField(
        label='RUC (opcional)',
        required=False,
        validators=[RegexValidator(
            regex=r'^\d{11}$', 
            message='El RUC debe contener 11 dígitos numéricos.'
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su RUC',
            'maxlength': 11
        })
    )

    class Meta:
        model = Cliente
        fields = [
            'dni', 'nombre_cliente', 'apellido_paterno', 
            'apellido_materno', 'email_cliente', 'telefono_cliente', 
            'direccion_cliente', 'ruc_cliente'
        ]

    def clean(self):
        """
        Validaciones adicionales de formulario
        """
        cleaned_data = super().clean()
        
        # Validación de DNI único
        dni = cleaned_data.get('dni')
        if dni and Cliente.objects.filter(dni=dni).exists():
            raise ValidationError({
                'dni': 'Ya existe un cliente registrado con este DNI.'
            })

        # Validación de que al menos un medio de contacto esté presente
        email = cleaned_data.get('email_cliente')
        telefono = cleaned_data.get('telefono_cliente')
        
        if not email and not telefono:
            raise ValidationError(
                'Debe proporcionar al menos un medio de contacto (email o teléfono).'
            )

        return cleaned_data

    def clean_nombre_cliente(self):
        """
        Normaliza el nombre (primera letra mayúscula)
        """
        nombre = self.cleaned_data['nombre_cliente']
        return nombre.strip().title()

    def clean_apellido_paterno(self):
        """
        Normaliza el apellido paterno
        """
        apellido = self.cleaned_data.get('apellido_paterno', '')
        return apellido.strip().title() if apellido else ''

    def clean_apellido_materno(self):
        """
        Normaliza el apellido materno
        """
        apellido = self.cleaned_data.get('apellido_materno', '')
        return apellido.strip().title() if apellido else ''
#### ---------------------------------------Proveedores--------------------------------------- ####

from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'contacto', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacto'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección', 'rows': 3}),
        }

    # Si necesitas validación adicional, puedes agregar métodos aquí.
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')
        return telefono

#### ---------------------------------------Compra--------------------------------------- ####
from django import forms
from .models import Compra

from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'fecha_compra', 'total_compra', 'documento_pdf']  # Se incluye fecha_compra
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_compra': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),  # Permite seleccionar la fecha
            'total_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documento_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),  # Widget para archivo
        }

    # Validación personalizada para total_compra
    def clean_total_compra(self):
        total = self.cleaned_data['total_compra']
        if total < 0:  # Permite 0 pero no valores negativos
            raise forms.ValidationError('El total de la compra no puede ser negativo.')
        return total



#### -                                       Detalle Compra
# Formulario para DetalleCompra

from django import forms
from .models import DetalleCompra

# Formulario para DetalleCompra
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['compra', 'producto', 'cantidad', 'precio_unitario']  # Campos que aparecerán en el formulario
        widgets = {
            'compra': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        

#### -                                       ventas

from django import forms
from .models import Venta, DetalleVenta

# Formulario para Venta
from django import forms
from .models import Venta, DetalleVenta, Cliente, TipoDocumento

from django import forms
from .models import Venta, DetalleVenta, Cliente, TipoDocumento

# Formulario mejorado para Venta
from django import forms
from .models import Venta, DetalleVenta, Cliente, TipoDocumento

# Formulario mejorado para Venta
class VentaForm(forms.ModelForm):
    # Cliente con búsqueda mejorada
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all().order_by('nombre_cliente'),
        widget=forms.Select(attrs={
            'class': 'form-control select2-cliente',
            'id': 'id_cliente',
            'data-placeholder': 'Buscar cliente por nombre o DNI',
        })
    )
    
    # Tipo de documento con Select2
    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select2-tipo-doc',
            'data-placeholder': 'Seleccione tipo de documento'
        })
    )
    
    # Campos editables normales
    numero_documento = forms.CharField(
        label="Número de documento",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese número de documento'
        })
    )
    
    cliente_nombre = forms.CharField(
        label="Nombre del cliente",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo del cliente'
        })
    )
    
    cliente_contacto = forms.CharField(
        label="Contacto del cliente",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono o correo de contacto'
        })
    )
    
    total_venta = forms.DecimalField(
        label="Total de la venta (S/.)",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    
    # Campo opcional para observaciones
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Observaciones o comentarios adicionales',
            'rows': 3
        })
    )

    class Meta:
        model = Venta
        fields = ['cliente', 'tipo_documento', 'numero_documento', 'cliente_nombre', 
                 'cliente_contacto', 'total_venta']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Añadimos etiquetas más descriptivas
        self.fields['cliente'].label = "Seleccione el cliente"
        self.fields['tipo_documento'].label = "Tipo de documento"
        self.fields['total_venta'].label = "Monto total (S/.)"

# ccc                                    Formulario para DetalleVenta
# class DetalleVentaForm(forms.ModelForm):
#     class Meta:
#         model = DetalleVenta
#         fields = ['producto', 'cantidad', 'precio_unitario']
#         widgets = {
#             'producto': forms.Select(attrs={'class': 'form-control'}),
#             'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
#             'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
#         }
# forms.py - Formulario mejorado
# from django import forms
# from .models import DetalleVenta, Venta, Producto

# from django import forms
# from django.core.exceptions import ValidationError
# from .models import DetalleVenta, Producto, Venta

# # Formulario original (mantener para compatibilidad con código existente)
# class DetalleVentaForm(forms.ModelForm):
#     class Meta:
#         model = DetalleVenta
#         fields = ['producto', 'cantidad', 'precio_unitario']
#         widgets = {
#             'producto': forms.Select(attrs={'class': 'form-control'}),
#             'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
#             'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

# # Formulario para validación AJAX de detalle de venta
# # Formulario para validación AJAX de detalle de venta
# class DetalleVentaAjaxForm(forms.Form):
#     producto_id = forms.IntegerField(min_value=1)
#     cantidad = forms.IntegerField(min_value=1)
#     precio_unitario = forms.DecimalField(min_value=0.01, decimal_places=2)
    
#     def clean(self):
#         cleaned_data = super().clean()
#         producto_id = cleaned_data.get('producto_id')
#         cantidad = cleaned_data.get('cantidad')
        
#         if producto_id and cantidad:
#             try:
#                 producto = Producto.objects.get(pk=producto_id)
#                 print(f"Validando producto ID {producto_id}: {producto.nombre_producto}")
#                 # Temporalmente desactivar la validación de stock para depuración
#                 # if cantidad > producto.stock:
#                 #     raise ValidationError(
#                 #         f'Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.stock}'
#                 #     )
#                 # Añadir el producto al cleaned_data para usarlo en la vista
#                 cleaned_data['producto'] = producto
#             except Producto.DoesNotExist:
#                 print(f"Error: Producto con ID {producto_id} no existe")
#                 raise ValidationError(f'El producto con ID {producto_id} no existe')
#             except Exception as e:
#                 print(f"Error inesperado al validar producto {producto_id}: {str(e)}")
#                 raise ValidationError(f'Error al procesar el producto: {str(e)}')
        
#         return cleaned_data

# # Formulario para actualizar el total de la venta
# class ActualizarTotalVentaForm(forms.ModelForm):
#     class Meta:
#         model = Venta
#         fields = ['total_venta']
from django import forms
from django.core.exceptions import ValidationError
from .models import DetalleVenta, Venta, Producto

# Configurar logger para mejor seguimiento de errores
from django import forms
from django.core.exceptions import ValidationError
from .models import DetalleVenta, Venta, Producto

from django import forms
from django.core.exceptions import ValidationError
from .models import DetalleVenta, Venta, Producto

# Formulario para búsqueda de productos
class ProductoSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Buscar productos',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre, marca o categoría...'
        })
    )

# Formulario para agregar un producto al carrito
class AgregarProductoForm(forms.Form):
    producto_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'placeholder': 'Cantidad'
        })
    )
    precio_unitario = forms.DecimalField(
        min_value=0.01,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0.01',
            'step': '0.01',
            'placeholder': 'Precio'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        producto_id = cleaned_data.get('producto_id')
        cantidad = cleaned_data.get('cantidad')
        
        if producto_id and cantidad and cantidad > 0:
            try:
                producto = Producto.objects.get(pk=producto_id)
                
                # Validar stock
                if cantidad > producto.stock:
                    self.add_error('cantidad', 
                        f'Stock insuficiente. Disponible: {producto.stock}')
                
                # Agregar el producto completo para usarlo en la vista
                cleaned_data['producto'] = producto
                
            except Producto.DoesNotExist:
                self.add_error('producto_id', 'El producto seleccionado no existe')
        
        return cleaned_data

# Formulario para edición de detalles existentes
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(
                attrs={
                    'class': 'form-control',
                    'data-placeholder': 'Seleccione un producto'
                }
            ),
            'cantidad': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'placeholder': 'Cantidad'
                }
            ),
            'precio_unitario': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0.01',
                    'step': '0.01',
                    'placeholder': 'Precio unitario'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimización: filtrar solo productos con stock
        # Para edición, incluimos también el producto actual aunque no tenga stock
        if self.instance and self.instance.pk and self.instance.producto:
            current_product = self.instance.producto
            self.fields['producto'].queryset = Producto.objects.filter(
                Q(stock__gt=0) | Q(pk=current_product.pk)
            ).order_by('nombre_producto')
        else:
            self.fields['producto'].queryset = Producto.objects.filter(
                stock__gt=0
            ).order_by('nombre_producto')
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        
        if producto and cantidad:
            # Para edición, necesitamos considerar la cantidad actual
            cantidad_actual = 0
            if self.instance and self.instance.pk and self.instance.producto == producto:
                cantidad_actual = self.instance.cantidad
            
            # Calcular el stock disponible considerando la cantidad actual
            stock_disponible = producto.stock + cantidad_actual
            
            # Validar stock disponible
            if cantidad > stock_disponible:
                self.add_error('cantidad', 
                    f'Stock insuficiente. Disponible: {stock_disponible}')
        
        return cleaned_data

# Formulario para eliminar un producto del carrito
class EliminarProductoForm(forms.Form):
    producto_index = forms.IntegerField(
        widget=forms.HiddenInput()
    )

# Formulario simple para finalizar la venta
class FinalizarVentaForm(forms.Form):
    confirmar = forms.BooleanField(
        required=True,
        initial=True,
        widget=forms.HiddenInput()
    )
# Formulario principal para DetalleVenta - ModelForm mejorado


###                                               tipo document

from django import forms
from .models import TipoDocumento

class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = ['tipo_documento']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
        }


#### ---------------------------------------Pedidos--------------------------------------- ####

### ---------------------------------------Calculadora--------------------------------------- ###

from django import forms
from .models import Producto

from django import forms
from .models import Producto, Categoria, Marca, TipoMotor

class FiltroProductosForm(forms.Form):
    busqueda = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre...', 'class': 'form-control'})
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        required=False,
        empty_label="Todas las marcas",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo_motor = forms.ModelChoiceField(
        queryset=TipoMotor.objects.all(),
        required=False,
        empty_label="Todos los tipos de motor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    precio_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Precio mínimo', 'class': 'form-control'})
    )
    precio_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Precio máximo', 'class': 'form-control'})
    )

class CalculadoraForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Productos seleccionados"
    )