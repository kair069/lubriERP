from django.db import models
from django.urls import reverse
from mi_app.models import Proveedor, Producto

class Pedido(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('pagado', 'Pagado'),  # Se cambió 'pegado' a 'pagado'
    ]

    proveedor = models.ForeignKey(
        Proveedor, 
        on_delete=models.CASCADE,
        verbose_name="Proveedor",
        help_text="Seleccione el proveedor de este pedido"
    )
    costo_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Costo Total",
        help_text="Costo total del pedido"
    )
    estado_pago = models.CharField(
        max_length=10, 
        choices=ESTADO_PAGO_CHOICES, 
        default='pendiente',
        verbose_name="Estado de Pago",
        help_text="Estado actual del pago"
    )
    fecha_pedido = models.DateField(
        verbose_name="Fecha de Pedido",
        help_text="Ingrese la fecha en que se realizó el pedido"
    )
    fecha_entrega = models.DateField(
        verbose_name="Fecha de Entrega",
        help_text="Ingrese la fecha estimada de entrega"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción del Pedido",
        help_text="Ingrese una descripción o comentarios adicionales sobre el pedido"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.proveedor.nombre_proveedor}"

    def actualizar_costo_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.costo_total = total
        self.save()

    def get_absolute_url(self):
        """
        Retorna la URL para ver el detalle del pedido.
        Se utiliza el nombre de la vista combinada 'pedido_combined_detail'.
        """
        return reverse('pedido_combined_detail', kwargs={'pk': self.pk})


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name='detalles',
        verbose_name="Pedido",
        help_text="Seleccione el pedido al que pertenece este detalle"
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        verbose_name="Producto",
        help_text="Seleccione el producto"
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name="Cantidad",
        help_text="Ingrese la cantidad de productos solicitados"
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio Unitario",
        help_text="Ingrese el precio unitario del producto"
    )

    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles del Pedido"
        ordering = ['producto__nombre_producto']  # Ordena por el nombre del producto

    def __str__(self):
        return f"{self.producto.nombre_producto} x {self.cantidad}"

    # @property
    # def subtotal(self):
    #     """Calcula y retorna el subtotal de este detalle."""
    #     return self.cantidad * self.precio_unitario
    @property
    def subtotal(self):
        """Calcula y retorna el subtotal de este detalle."""
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        """Al guardar, actualizar el costo total del pedido."""
        super().save(*args, **kwargs)
        self.pedido.actualizar_costo_total()

    def delete(self, *args, **kwargs):
        """Al eliminar, actualizar el costo total del pedido."""
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido.actualizar_costo_total()
