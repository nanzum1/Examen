from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from inventario import views

urlpatterns = [
    # Vista principal (inicio)
    path('', views.inicio, name='inicio'),

    # Rutas de autenticación
    path('usuarios_ingresar/', auth_views.LoginView.as_view(), name='login'),
    path('usuarios_salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios_nuevo/', views.register, name='register'),

    # Rutas de películas
    path('peliculas/', views.listar_peliculas, name='peliculas'),
    path('peliculas/<int:pk>/detalle/', views.detalle_pelicula, name='detalle_pelicula'),
    path('peliculas/nueva/', views.agregar_pelicula, name='agregar_pelicula'),
    path('peliculas/<int:pk>/editar/', views.editar_pelicula, name='editar_pelicula'),
    path('peliculas/<int:pk>/eliminar/', views.eliminar_pelicula, name='eliminar_pelicula'),

    # Rutas de transacciones
    path('transacciones/', views.listar_transacciones, name='listar_transacciones'),
    path('transacciones/<int:pk>/', views.detalle_transaccion, name='detalle_transaccion'),
    path('transacciones/nueva/<int:pk>/', views.nueva_transaccion, name='nueva_transaccion'),
]
