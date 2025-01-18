from django.contrib import admin
from .models import Pelicula, Transaccion


# Registra los modelos en el panel de administración
admin.site.register(Pelicula)
admin.site.register(Transaccion)

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm

# Personaliza el formulario de creación de usuarios
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Usa el formulario personalizado
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Registra el modelo User con el formulario personalizado
admin.site.unregister(User)  # Primero desregistramos el modelo User original
admin.site.register(User, CustomUserAdmin)  # Lo registramos de nuevo con el formulario personalizado

