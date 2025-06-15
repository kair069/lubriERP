from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la vista de registro de usuario
    # Ruta para el registro de usuarios
    path('registro/', views.registro_usuario, name='registro_usuario'),
    
    # Ruta para el login de usuarios
    path('login/', views.login_usuario, name='login_usuario'),
    
    # Ruta para el logout de usuarios
    path('logout/', views.logout_usuario, name='logout_usuario'),
    
    # Ruta para el panel del usuario (dashboard)
    path('dashboard/', views.dashboard, name='dashboard'),
]