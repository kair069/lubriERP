from django import forms
from .models import Pedido, DetallePedido
from django import forms
from django.core.exceptions import ValidationError
from .models import Pedido

class PedidoForm(forms.ModelForm):
    # Campos para búsqueda avanzada
    proveedor_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar proveedor por nombre, contacto o email',
            'id': 'proveedor-search'
        }),
        label="Buscar Proveedor"
    )

    class Meta:
        model = Pedido
        fields = [
            'proveedor', 
            'estado_pago', 
            'fecha_pedido', 
            'fecha_entrega', 
            'descripcion'
        ]
        widgets = {
            'proveedor': forms.Select(attrs={
                'class': 'form-control proveedor-select',
                'data-placeholder': 'Seleccione un proveedor'
            }),
            'estado_pago': forms.Select(attrs={
                'class': 'form-control estado-pago-select',
                'data-placeholder': 'Seleccione un estado de pago'
            }),
            'fecha_pedido': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD'
            }),
            'fecha_entrega': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese una descripción o comentarios sobre el pedido...'
            }),
        }

    def clean(self):
        """Validaciones personalizadas para el pedido"""
        cleaned_data = super().clean()
        fecha_pedido = cleaned_data.get('fecha_pedido')
        fecha_entrega = cleaned_data.get('fecha_entrega')
        
        # Validaciones de fechas
        if fecha_pedido and fecha_entrega:
            if fecha_entrega < fecha_pedido:
                raise ValidationError({
                    'fecha_entrega': 'La fecha de entrega no puede ser anterior a la fecha de pedido.'
                })
            
            # Limitar pedidos a un año en el futuro
            max_fecha_entrega = fecha_pedido.replace(year=fecha_pedido.year + 1)
            if fecha_entrega > max_fecha_entrega:
                raise ValidationError({
                    'fecha_entrega': 'La fecha de entrega no puede estar más de un año en el futuro.'
                })
        
        return cleaned_data
# class PedidoForm(forms.ModelForm):
#     class Meta:
#         model = Pedido
#         # Lista de campos que se mostrarán en el formulario.
#         # Se omite 'costo_total' ya que normalmente se calcula automáticamente.
#         fields = [
#             'proveedor', 
#             'estado_pago', 
#             'fecha_pedido', 
#             'fecha_entrega', 
#             'descripcion'
#         ]
#         widgets = {
#             'proveedor': forms.Select(attrs={
#                 'class': 'form-control',
#             }),
#             'estado_pago': forms.Select(attrs={
#                 'class': 'form-control',
#             }),
#             'fecha_pedido': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date',  # HTML5 datepicker
#                 'placeholder': 'YYYY-MM-DD'
#             }),
#             'fecha_entrega': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date',
#                 'placeholder': 'YYYY-MM-DD'
#             }),
#             'descripcion': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3,
#                 'placeholder': 'Ingrese una descripción o comentarios sobre el pedido...'
#             }),
#         }
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Pedido

# class PedidoForm(forms.ModelForm):
#     class Meta:
#         model = Pedido
#         fields = [
#             'proveedor', 
#             'estado_pago', 
#             'fecha_pedido', 
#             'fecha_entrega', 
#             'descripcion'
#         ]
        
#         widgets = {
#             'proveedor': forms.Select(attrs={
#                 'class': 'form-control select2',
#                 'placeholder': 'Seleccione un proveedor'
#             }),
#             'estado_pago': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Seleccione el estado de pago'
#             }),
#             'fecha_pedido': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date',
#                 'placeholder': 'YYYY-MM-DD'
#             }),
#             'fecha_entrega': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date',
#                 'placeholder': 'YYYY-MM-DD'
#             }),
#             'descripcion': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3,
#                 'placeholder': 'Ingrese una descripción o comentarios sobre el pedido...',
#                 'maxlength': 500
#             }),
#         }

#     def clean_fecha_pedido(self):
#         """
#         Validación para asegurar que la fecha de pedido no sea en el futuro
#         """
#         fecha_pedido = self.cleaned_data.get('fecha_pedido')
        
#         if fecha_pedido and fecha_pedido > timezone.now().date():
#             raise ValidationError("La fecha de pedido no puede ser en el futuro.")
        
#         return fecha_pedido

#     def clean_fecha_entrega(self):
#         """
#         Validación para asegurar que la fecha de entrega sea posterior a la fecha de pedido
#         """
#         fecha_pedido = self.cleaned_data.get('fecha_pedido')
#         fecha_entrega = self.cleaned_data.get('fecha_entrega')
        
#         if fecha_pedido and fecha_entrega:
#             if fecha_entrega < fecha_pedido:
#                 raise ValidationError("La fecha de entrega debe ser posterior a la fecha de pedido.")
        
#         return fecha_entrega

#     def clean_descripcion(self):
#         """
#         Validación para la descripción
#         """
#         descripcion = self.cleaned_data.get('descripcion', '')
        
#         # Ejemplo de validación: longitud mínima
#         if descripcion and len(descripcion) < 10:
#             raise ValidationError("La descripción debe tener al menos 10 caracteres.")
        
#         return descripcion

#     def __init__(self, *args, **kwargs):
#         """
#         Personalización adicional del formulario
#         """
#         super().__init__(*args, **kwargs)
        
#         # Hacer campos obligatorios
#         self.fields['proveedor'].required = True
#         self.fields['estado_pago'].required = True
#         self.fields['fecha_pedido'].required = True
#         self.fields['fecha_entrega'].required = True
        
#         # Añadir help_text
#         self.fields['proveedor'].help_text = 'Seleccione el proveedor del pedido'
#         self.fields['estado_pago'].help_text = 'Indique el estado actual del pago'
#         self.fields['fecha_pedido'].help_text = 'Fecha en que se realizó el pedido'
#         self.fields['fecha_entrega'].help_text = 'Fecha estimada de entrega'
#         self.fields['descripcion'].help_text = 'Comentarios adicionales (máximo 500 caracteres)'

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        # Excluimos 'pedido' ya que se asigna desde la vista o se maneja mediante un Inline.
        fields = ['producto', 'cantidad', 'precio_unitario']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario'    ,
        }
        help_texts = {
            'producto': 'Seleccione el producto que desea agregar al pedido.',
            'cantidad': 'Ingrese la cantidad deseada (mínimo 1).',
            'precio_unitario': 'Ingrese el precio unitario actual del producto.',
        }
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ingrese la cantidad'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ingrese el precio unitario'
            }),
        }
