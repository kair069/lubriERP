# utils.py
from django.utils import timezone
import datetime
from .models import Venta, TipoDocumento

def generar_numero_documento(tipo_documento):
    """
    Genera un número de documento secuencial basado en el tipo y la fecha actual
    
    Args:
        tipo_documento (str): El tipo de documento ('Factura' o 'Boleta')
        
    Returns:
        str: Número de documento generado
    """
    # Obtiene la fecha actual
    hoy = timezone.now().date()
    year = hoy.strftime("%Y")
    month = hoy.strftime("%m")
    
    # Determina el prefijo según el tipo de documento
    prefijo = "B" if tipo_documento == "Boleta" else "F"
    
    # Busca el último documento de este tipo en el mes actual
    documentos_recientes = Venta.objects.filter(
        tipo_documento__tipo_documento=tipo_documento,
        fecha_venta__year=hoy.year,
        fecha_venta__month=hoy.month
    ).order_by('-numero_documento')
    
    # Si hay documentos previos, incrementa el último
    if documentos_recientes.exists():
        ultimo_documento = documentos_recientes.first().numero_documento
        # Busca la parte numérica al final del documento
        partes = ultimo_documento.split('-')
        if len(partes) > 1:
            try:
                ultimo_numero = int(partes[-1])
                numero_nuevo = ultimo_numero + 1
            except ValueError:
                # Si no es un número válido, comienza en 1
                numero_nuevo = 1
        else:
            numero_nuevo = 1
    else:
        # Si no hay documentos, comienza en 1
        numero_nuevo = 1
    
    # Formatea el número con ceros a la izquierda (6 dígitos)
    numero_formateado = f"{numero_nuevo:06d}"
    
    # Construye el número completo: [Prefijo]-[Año][Mes]-[Número]
    numero_documento = f"{prefijo}-{year}{month}-{numero_formateado}"
    
    return numero_documento

def calcular_monto_total(detalles):
    """
    Calcula el monto total a partir de una lista de detalles de venta
    
    Args:
        detalles (list): Lista de objetos DetalleVenta
        
    Returns:
        Decimal: Monto total calculado
    """
    from decimal import Decimal
    total = Decimal('0.00')
    
    for detalle in detalles:
        if detalle.subtotal:
            total += detalle.subtotal
    
    return total