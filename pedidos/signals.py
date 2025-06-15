from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetallePedido

@receiver(post_save, sender=DetallePedido)
def actualizar_costo_al_guardar(sender, instance, **kwargs):
    """Actualiza el costo total del pedido al guardar un detalle."""
    instance.pedido.actualizar_costo_total()

@receiver(post_delete, sender=DetallePedido)
def actualizar_costo_al_eliminar(sender, instance, **kwargs):
    """Actualiza el costo total del pedido al eliminar un detalle."""
    instance.pedido.actualizar_costo_total()
