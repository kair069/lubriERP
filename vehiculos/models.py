from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.nombre}"

class Motor(models.Model):
    cilindrada = models.CharField(max_length=50)
    potencia = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cilindrada} - {self.potencia}"

class TipoCombustible(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Transmision(models.Model):
    tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipo

class Vehiculo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    año = models.IntegerField()
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    tipo_combustible = models.ForeignKey(TipoCombustible, on_delete=models.CASCADE)
    transmision = models.ForeignKey(Transmision, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='vehiculos/', null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"

class FiltroAceite(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100)
    compatible_con = models.ManyToManyField(Vehiculo)

    def __str__(self):
        return f"Filtro Aceite {self.codigo} ({self.marca})"

class FiltroCombustible(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100)
    compatible_con = models.ManyToManyField(Vehiculo)

    def __str__(self):
        return f"Filtro Combustible {self.codigo} ({self.marca})"

class FiltroAire(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100)
    compatible_con = models.ManyToManyField(Vehiculo)

    def __str__(self):
        return f"Filtro Aire {self.codigo} ({self.marca})"

class Aceite(models.Model):
    tipo = models.CharField(max_length=100)
    viscosidad = models.CharField(max_length=50)
    marca = models.CharField(max_length=100)
    compatible_con = models.ManyToManyField(Vehiculo)

    def __str__(self):
        return f"Aceite {self.marca} {self.tipo} {self.viscosidad}"

class UbicacionParte(models.Model):
    nombre_parte = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen_url = models.URLField()
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_parte} - {self.vehiculo}"
