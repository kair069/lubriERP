from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    # Sobrescribimos el campo password para que tenga un campo de confirmación de contraseña
    password = forms.CharField(widget=forms.PasswordInput, max_length=255, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=255, label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password']  # No incluimos 'estado' ni 'fecha_creacion'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Comprobamos si las contraseñas coinciden
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        # Llamamos al método save del modelo para guardar la instancia
        usuario = super().save(commit=False)
        if usuario.password:
            usuario.set_password(usuario.password)  # Encriptamos la contraseña
        if commit:
            usuario.save()
        return usuario
