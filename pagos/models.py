from django.db import models

# Create your models here.
from django.db import models

class Proveedor(models.Model):
    TIPO_CHOICES = [
        ('Servicio Público', 'Servicio Público'),
        ('Impuesto', 'Impuesto'),
        ('Proveedor Privado', 'Proveedor Privado'),
    ]

    nombre = models.CharField(max_length=150, verbose_name="Nombre del Proveedor")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Proveedor")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    contacto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contacto")

    def __str__(self):
        return self.nombre

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    METODO_CHOICES = [
        ('BCP', 'BCP'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Vencido', 'Vencido'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedor")
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE, verbose_name="Categoría de Gasto")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    fecha_pago = models.DateTimeField(verbose_name="Fecha de Pago")
    metodo_pago = models.CharField(max_length=15, choices=METODO_CHOICES, verbose_name="Método de Pago")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, verbose_name="Estado del Pago")
    comprobante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comprobante")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas")

    def __str__(self):
        return f"{self.proveedor} - {self.monto} ({self.estado})"

class ArbitriosMunicipales(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
    ]

    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    fecha_pago = models.DateTimeField(verbose_name="Fecha de Pago")
    municipio = models.CharField(max_length=150, verbose_name="Municipio")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, verbose_name="Estado del Pago")

    def __str__(self):
        return f"{self.municipio} - {self.monto} ({self.estado})"

class Usuario(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Usuario")
    email = models.EmailField(max_length=150, unique=True, verbose_name="Correo Electrónico")

    def __str__(self):
        return self.nombre
