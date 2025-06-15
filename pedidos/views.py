from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
)
from .models import Pedido, DetallePedido
from .forms import PedidoForm, DetallePedidoForm

# ============================
# Vistas para Pedido
# ============================

class PedidoListView(ListView):
    model = Pedido
    template_name = 'mi__app/pedidos/pedido_list.html'  # Plantilla para listar pedidos
    context_object_name = 'pedidos'
    ordering = ['-fecha_pedido']  # Lista los pedidos ordenados por fecha descendente

class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'mi__app/pedidos/pedido_form.html'  # Se usará la misma plantilla para crear y editar

    def form_valid(self, form):
        """Método que se ejecuta cuando el formulario es válido."""
        response = super().form_valid(form)
        # Se actualiza el costo total del pedido si es necesario
        self.object.actualizar_costo_total()
        return response

class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'mi__app/pedidos/pedido_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.actualizar_costo_total()
        return response

class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'mi__app/pedidos/pedido_confirm_delete.html'  # Plantilla para confirmar la eliminación
    success_url = reverse_lazy('pedido_list')  # Redirige a la lista de pedidos luego de borrar

# Vista combinada para mostrar la información del pedido y sus detalles
class PedidoCombinedDetailView(TemplateView):
    template_name = 'mi__app/pedidos/pedido_combined_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_id = self.kwargs.get('pk')
        pedido = Pedido.objects.get(pk=pedido_id)
        detalles = pedido.detalles.all()  # Se usa el related_name definido en el modelo DetallePedido
        context['pedido'] = pedido
        context['detalles'] = detalles
        return context

# ============================
# Vistas para DetallePedido
# ============================

class DetallePedidoListView(ListView):
    model = DetallePedido
    template_name = 'mi__app/detallepedido/detallepedido_list.html'
    context_object_name = 'detalles'
    ordering = ['pedido']  # Ajusta el orden según convenga

class DetallePedidoDetailView(DetailView):
    model = DetallePedido
    template_name = 'mi__app/detallepedido/detallepedido_detail.html'
    context_object_name = 'detalle'

class DetallePedidoCreateView(CreateView):
    model = DetallePedido
    form_class = DetallePedidoForm
    template_name = 'mi__app/detallepedido/detallepedido_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se espera que la URL incluya el id del pedido al que se agregará el detalle
        context['pedido_id'] = self.kwargs.get('pedido_id')
        return context

    def form_valid(self, form):
        # Asigna el pedido recibido en la URL al detalle antes de guardarlo
        pedido_id = self.kwargs.get('pedido_id')
        form.instance.pedido_id = pedido_id
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige a la vista combinada del pedido luego de crear el detalle
        return reverse('pedido_combined_detail', kwargs={'pk': self.object.pedido.pk})

class DetallePedidoUpdateView(UpdateView):
    model = DetallePedido
    form_class = DetallePedidoForm
    template_name = 'mi__app/detallepedido/detallepedido_form.html'

    def get_success_url(self):
        # Redirige a la vista combinada del pedido luego de actualizar el detalle
        return reverse('pedido_combined_detail', kwargs={'pk': self.object.pedido.pk})

class DetallePedidoDeleteView(DeleteView):
    model = DetallePedido
    template_name = 'mi__app/detallepedido/detallepedido_confirm_delete.html'

    def get_success_url(self):
        # Redirige a la vista combinada del pedido luego de borrar el detalle
        return reverse_lazy('pedido_combined_detail', kwargs={'pk': self.object.pedido.pk})



### En este archivo se definen las vistas para manejar los pedidos y sus detalles.
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from mi_app.models import Producto

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from mi_app.models import Producto

@require_GET
def obtener_precio_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'precio': float(producto.precio),
            'success': True
        })
    except Producto.DoesNotExist:
        return JsonResponse({
            'precio': None, 
            'success': False
        })