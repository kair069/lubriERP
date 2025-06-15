from arrow import now
from django.db import models
from jsonschema import ValidationError



# Tabla de Marcas
class Marca(models.Model):
    nombre_marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_marca

# Tabla de Categorías
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_categoria

# Tabla de Tipos de Motor
class TipoMotor(models.Model):
    GASOLINERO = 'Gasolinero'
    PETROLERO = 'Petrolero'
    
    TIPO_CHOICES = [
        (GASOLINERO, 'Gasolinero'),
        (PETROLERO, 'Petrolero'),
    ]
    
    tipo_motor = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.tipo_motor

# Tabla de Tipos de Productos
class TipoProducto(models.Model):
    nombre_tipo_producto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo_producto

# Tabla de Proveedores
class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre_proveedor

# Tabla de Clientes
from django.db import models

class Cliente(models.Model):
    dni = models.CharField(max_length=8, unique=True)  # DNI del cliente
    nombre_cliente = models.CharField(max_length=150)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    contacto_cliente = models.CharField(max_length=100, blank=True, null=True)
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)
    email_cliente = models.EmailField(blank=True, null=True)
    direccion_cliente = models.CharField(max_length=255, blank=True, null=True)
    ruc_cliente = models.CharField(max_length=20, blank=True, null=True)  # RUC si es necesario
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_cliente} ({self.dni})"


# Tabla de Productos
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=150)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo_motor = models.ForeignKey(TipoMotor, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_producto

# Relación entre Productos y Tipos de Productos
class ProductoTipo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.tipo_producto.nombre_tipo_producto}"

from decimal import Decimal

# Tabla de Compras
# Modelo de Compras
class Compra(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(default=now)  # Se asigna la fecha actual por defecto, pero es editable
    total_compra = models.DecimalField(max_digits=10, decimal_places=2)
    documento_pdf = models.FileField(upload_to='documentos_compras/', blank=True, null=True)  # Campo para el PDF

    def __str__(self):
        return f"Compra {self.id} - {self.fecha_compra.strftime('%Y-%m-%d %H:%M:%S')}"


# Tabla de Detalles de Compras
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.cantidad) * Decimal(self.precio_unitario)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre_producto}"


# Tabla de Tipos de Documentos
class TipoDocumento(models.Model):
    BOLETA = 'Boleta'
    FACTURA = 'Factura'
    
    TIPO_CHOICES = [
        (BOLETA, 'Boleta'),
        (FACTURA, 'Factura'),
    ]

    tipo_documento = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.tipo_documento

# Tabla de Ventas
class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=150)
    cliente_contacto = models.CharField(max_length=100, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Venta {self.numero_documento}"

# Tabla de Detalles de Ventas
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre_producto}"

# Tabla de Boletas de Venta
class BoletaVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_boleta = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_boleta

# Tabla de Facturas
class Factura(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    ruc_cliente = models.CharField(max_length=20, blank=True, null=True)
    direccion_cliente = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.numero_factura

# Tabla de Cambios de Aceite
class CambioAceite(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    kilometraje = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_aceite = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    numero_voucher = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Cambio de aceite {self.id_cambio_aceite} - {self.cliente.nombre_cliente}"


#####                                                Pedidos
