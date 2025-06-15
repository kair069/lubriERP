from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ArbitriosMunicipales
from .forms import ArbitriosMunicipalesForm

# 📋 LISTAR ARBITRIOS MUNICIPALES
class ArbitriosMunicipalesListView(ListView):
    model = ArbitriosMunicipales
    template_name = 'arbitrios/lista.html'
    context_object_name = 'arbitrios'

# 🔍 DETALLE DE UN ARBITRIO MUNICIPAL
class ArbitriosMunicipalesDetailView(DetailView):
    model = ArbitriosMunicipales
    template_name = 'arbitrios/detalle.html'
    context_object_name = 'arbitrio'

# ➕ CREAR UN NUEVO ARBITRIO MUNICIPAL
class ArbitriosMunicipalesCreateView(CreateView):
    model = ArbitriosMunicipales
    form_class = ArbitriosMunicipalesForm
    template_name = 'arbitrios/formulario.html'
    success_url = reverse_lazy('arbitrios_lista')

# ✏️ EDITAR UN ARBITRIO MUNICIPAL
class ArbitriosMunicipalesUpdateView(UpdateView):
    model = ArbitriosMunicipales
    form_class = ArbitriosMunicipalesForm
    template_name = 'arbitrios/formulario.html'
    success_url = reverse_lazy('arbitrios_lista')

# 🗑️ ELIMINAR UN ARBITRIO MUNICIPAL
class ArbitriosMunicipalesDeleteView(DeleteView):
    model = ArbitriosMunicipales
    template_name = 'arbitrios/confirmar_eliminacion.html'
    success_url = reverse_lazy('arbitrios_lista')
