import pandas as pd
import numpy as np
import unidecode
import re
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Datos de inventario
data = {
    "ID": [61, 62, 63, 64, 65, 66],
    "Nombre": [
        "SHELL HELIX HX8 PROFESSIONAL GALON 5W-30",
        "CASTROL MAGNATEC GASOLINA DIESEL GALON FULL SINTETICO 5W-30",
        "MOTTOR BRAKE LIQUIDO DE FRENOS AZUL 355ml DOT 3",
        "MOBIL 1 GALON 0W-40",
        "MOBIL 1 FULL SINTETICO GALON 5W-50",
        "MOBIL 1 GALON 5W-30"
    ],
    "Stock": [3, 2, 1, 3, 2, 2],
    "Precio": [195, 195, 15, 135, 130, 40],
    "Precio_Competencia": [190, 200, 14, 130, 125, 38],
    "Ventas_Historicas": [5, 6, 4, 7, 5, 6],
    "Stock_Competencia": [50, 60, 45, 40, 55, 30],
    "Condiciones_Economicas": [0.9, 1.1, 1.05, 0.95, 1.2, 1.1],
    "Campañas_Marketing": [1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# Entrenar modelo Random Forest
def entrenar_modelo():
    X = df[["Stock", "Precio", "Precio_Competencia", "Stock_Competencia", "Condiciones_Economicas", "Campañas_Marketing"]]
    y = df["Ventas_Historicas"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model

modelo_rf = entrenar_modelo()

# Normalizar nombres
def limpiar_texto(texto):
    texto = unidecode.unidecode(texto.lower())
    texto = re.sub(r'[^a-z0-9 ]', '', texto)
    return texto.strip()

productos_normalizados = {limpiar_texto(nombre): nombre for nombre in df["Nombre"]}

# Función chatbot
def chatbot_respuesta(pregunta):
    pregunta_limpia = limpiar_texto(pregunta)
    
    # Buscar coincidencia exacta con mayor similaridad
    mejor_match = None
    max_similitud = 0
    
    for producto_limpio, producto_original in productos_normalizados.items():
        similitud = sum(1 for palabra in pregunta_limpia.split() if palabra in producto_limpio)
        
        if similitud > max_similitud:
            mejor_match = producto_original
            max_similitud = similitud

    if mejor_match is None:
        return "No entendí la pregunta o el producto no está en mi base de datos."
    
    stock_actual = df.loc[df["Nombre"] == mejor_match, "Stock"].values[0]
    datos_producto = df[df["Nombre"] == mejor_match][["Stock", "Precio", "Precio_Competencia", "Stock_Competencia", "Condiciones_Economicas", "Campañas_Marketing"]]
    demanda_futura = int(modelo_rf.predict(datos_producto)[0])
    
    reposicion = max(0, demanda_futura - stock_actual)
    return f"Se estima que venderás {demanda_futura} unidades de '{mejor_match}' el próximo mes. Actualmente tienes {stock_actual} en stock. Se recomienda reponer {reposicion} unidades."


# API para Django
@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pregunta = data.get("pregunta", "")
            respuesta = chatbot_respuesta(pregunta)
            return JsonResponse({"respuesta": respuesta})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"mensaje": "Método no permitido"}, status=405)




from django.shortcuts import render

def chatbot_page(request):
    return render(request, "chatbot1/chatbot.html")