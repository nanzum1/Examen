from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Pelicula, Transaccion
from .forms import PeliculaForm, CustomUserCreationForm, SignInForm, PeliculaForm

def inicio(request):
    return render(request, 'inicio.html', {'mensaje': '¡Bienvenido al sistema de gestión de películas!'})

def lista_usuario(request):
    if request.user.has_perm('auth.view_user'):
        usuarios = User.objects.all()
    else:
        usuarios = User.objects.filter(id=request.user.id)
    return render(request, 'inventario/usuarios_lista.html', {'usuarios': usuarios})

def nuevo_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios_nuevo.html', {'form': form})

def login_usuario(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_usuarios')
            else:
                return render(request, '/usuarios_ingresar.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
    return render(request, '/usuarios_ingresar.html', {'form': form})

def logout_view(request):
    logout(request) 
    messages.success(request, "Has cerrado sesión correctamente.") 
    return redirect('login') 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión al crear el usuario
            return redirect('peliculas')  # Redirigir a peliculas
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def listar_peliculas(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'peliculas_lista.html', {'peliculas': peliculas})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Pelicula, Transaccion

def detalle_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        tipo_transaccion = request.POST.get('tipo')

        if tipo_transaccion == 'AR' and pelicula.stock > 0:  # Arriendo
            pelicula.stock -= 1
            pelicula.save()
            Transaccion.objects.create(
                usuario=request.user,
                pelicula=pelicula,
                tipo='AR',
                fecha_inicio=timezone.now(),
                fecha_termino=timezone.now(),
                estado='CP'  # Completada
            )
            messages.success(request, 'Transacción de arriendo realizada exitosamente.')
        elif tipo_transaccion == 'CO' and pelicula.stock > 0:  # Compra
            pelicula.stock -= 1
            pelicula.save()
            Transaccion.objects.create(
                usuario=request.user,
                pelicula=pelicula,
                tipo='CO',
                fecha_inicio=timezone.now(),
                fecha_termino=timezone.now(),
                estado='CP'  # Completada
            )
            messages.success(request, 'Compra realizada exitosamente.')
        else:
            messages.error(request, 'No hay stock disponible para la transacción.')

    return render(request, 'pelicula_detalle.html', {'pelicula': pelicula})

def agregar_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('peliculas')
    else:
        form = PeliculaForm()
    return render(request, '/peliculas_nuevo.html/', {'form': form})

def editar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('peliculas')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'peliculas_editar.html', {'form': form})

def eliminar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        pelicula.delete()
        return redirect('peliculas')
    return render(request, 'peliculas_eliminar.html', {'pelicula': pelicula})

from .models import Transaccion

def listar_transacciones(request):
    if request.user.is_staff:
        transacciones = Transaccion.objects.all()
    else:
        transacciones = Transaccion.objects.filter(usuario=request.user)
    return render(request, 'transacciones_lista.html', {'transacciones': transacciones})

def detalle_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    return render(request, 'transacciones_detalle.html', {'transaccion': transaccion})

from django.utils import timezone
from .models import Pelicula, Transaccion


from django.utils import timezone

def nueva_transaccion(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    
    if request.method == 'POST':
        tipo_transaccion = request.POST.get('tipo')
        
        if tipo_transaccion == 'AR' and pelicula.stock > 0:  # Arriendo
            pelicula.stock -= 1
            pelicula.save()
            Transaccion.objects.create(
                usuario=request.user,
                pelicula=pelicula,
                tipo='AR',
                fecha_inicio=timezone.now(),
                fecha_termino=timezone.now(),  # Para arriendo, puedes colocar una fecha predeterminada
                estado='CP'  # Completada
            )
            messages.success(request, 'Transacción de arriendo realizada exitosamente.')
        elif tipo_transaccion == 'CO' and pelicula.stock > 0:  # Compra
            pelicula.stock -= 1
            pelicula.save()
            Transaccion.objects.create(
                usuario=request.user,
                pelicula=pelicula,
                tipo='CO',
                fecha_inicio=timezone.now(),
                estado='CP'  # Completada
            )
            messages.success(request, 'Compra realizada exitosamente.')
        else:
            messages.error(request, 'No hay stock disponible para la transacción.')

    return redirect('detalle_pelicula', pk=pk)



from django.contrib.auth.decorators import permission_required

@permission_required('inventario.add_pelicula', raise_exception=True)
def agregar_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pelicula agregada con éxito.')
            return redirect('peliculas')
    else:
        form = PeliculaForm()
    return render(request, 'peliculas_form.html', {'form': form})


