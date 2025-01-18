from django.contrib.auth.models import User
from django.db import models


# Modelo Pelicula
class Pelicula(models.Model):
    GENEROS = [
        ('CF', 'Ciencia Ficción'),
        ('TE', 'Terror'),
        ('SU', 'Suspenso'),
        ('RO', 'Romántica'),
        ('CO', 'Comedia'), 
        ('AC', 'Acción'), 
        ('DR', 'Drama'), 
        ('CR', 'Crimen'), 
        ('AN', 'Animación')
    ]

    titulo = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    genero = models.CharField(max_length=2, choices=GENEROS)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_arriendo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

# Modelo Transaccion
class Transaccion(models.Model):
    TIPOS = [
        ('AR', 'Arriendo'),
        ('CO', 'Compra'),
    ]
    ESTADOS = [
        ('CP', 'Completada'),
        ('PD', 'Pendiente'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPOS)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADOS)

    def __str__(self):
        return f"{self.tipo} - {self.usuario.username} - {self.pelicula.titulo}"
