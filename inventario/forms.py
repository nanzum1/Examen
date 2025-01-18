from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Pelicula, Transaccion


class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'director', 'genero', 'precio_compra', 'precio_arriendo', 'stock']
        widgets = {
            'genero': forms.Select(choices=Pelicula.GENEROS),
        }
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class SignInForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = '__all__'
    
class TransaccionUsuarioForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['usuario', 'pelicula', 'fecha_inicio', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['usuario', 'pelicula']:
            self.fields[field].disabled = True