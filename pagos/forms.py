from django import forms
from .models import ArbitriosMunicipales

class ArbitriosMunicipalesForm(forms.ModelForm):
    class Meta:
        model = ArbitriosMunicipales
        fields = ['monto', 'fecha_pago', 'municipio', 'estado']
        labels = {
            'monto': '💰 Monto Pagado',
            'fecha_pago': '📅 Fecha de Pago',
            'municipio': '🏛️ Municipio',
            'estado': '📌 Estado del Pago',
        }
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el monto'}),
            'fecha_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del municipio'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

