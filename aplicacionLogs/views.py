from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm
from .models import Usuario

# Vista para el registro de usuarios
def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario con la contraseña encriptada
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login_usuario')  # Redirige a la página de login después del registro
    else:
        form = UsuarioForm()

    return render(request, 'registro.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm
from .models import Usuario

# Vista para el registro de usuarios
def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario con la contraseña encriptada
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login_usuario')  # Redirige a la página de login después del registro
    else:
        form = UsuarioForm()

    return render(request, 'registro.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

# Vista para el logout
def logout_usuario(request):
    logout(request)  # Cierra la sesión del usuario
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login_usuario')  # Redirige al login después de cerrar sesión

from django.shortcuts import render, redirect

# Vista del panel de usuario
def dashboard(request):
    if not request.user.is_authenticated:  # Verifica si el usuario está autenticado
        return redirect('login_usuario')  # Redirige al login si no está autenticado
    return render(request, 'alex.html', {'usuario': request.user})  # Renderiza el dashboard


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

# Vista para el login
def login_usuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Autenticación del usuario (comparar email y contraseña encriptada)
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.check_password(password):  # Verificamos la contraseña encriptada
                login(request, usuario)  # Iniciamos sesión con el usuario autenticado
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('home')  # Redirige al dashboard del usuario
            else:
                messages.error(request, 'Credenciales incorrectas. Por favor, intente de nuevo.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas. Por favor, intente de nuevo.')

    return render(request, 'login.html')
