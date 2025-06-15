from django.db import models

# Create your models here.
from django.db import models

class Mensaje(models.Model):
    usuario = models.CharField(max_length=255)
    texto = models.TextField()
    respuesta = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    producto_relacionado = models.CharField(max_length=255, null=True, blank=True)
    demanda_estimada = models.IntegerField(null=True, blank=True)
    stock_actual = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario}: {self.texto[:50]}"
