from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Modelo: Usuario
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password

# Crear un Manager personalizado para el modelo de Usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con un correo electrónico y una contraseña."""
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)  # Encriptar la contraseña
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea un superusuario con privilegios."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Modelo de Usuario personalizado
class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)  # Activo o Inactivo
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)  # Este campo es importante para autenticación
    is_active = models.BooleanField(default=True)  # Indicar si el usuario está activo

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'  # Usamos el email como identificador
    REQUIRED_FIELDS = ['nombre']  # Campos que deben ser requeridos al crear un superusuario

    def __str__(self):
        return self.nombre

    # Método para establecer la contraseña de manera segura
    def set_password(self, password):
        self.password = make_password(password)  # Encriptar la contraseña

    # Método para verificar la contraseña
    def check_password(self, password):
        return check_password(password, self.password)  # Verificar la contraseña



# Modelo: Rol
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_rol

# Modelo intermedio: UsuarioRol
class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'rol')

# Modelo: Permiso
class Permiso(models.Model):
    nombre_permiso = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_permiso

# Modelo intermedio: RolPermiso
class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')

# Modelo: RecuperacionContrasena
class RecuperacionContrasena(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    fecha_expiracion = models.DateTimeField()
    usado = models.BooleanField(default=False)

    def __str__(self):
        return f"Recuperación de {self.usuario.nombre}"
