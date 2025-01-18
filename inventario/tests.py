from django.test import TestCase
from .models import Pelicula

class PeliculaTestCase(TestCase):
    def setUp(self):
        Pelicula.objects.create(
            titulo="Pelicula de prueba",
            director="Director de prueba",
            genero="CF",
            precio_compra=1000,
            precio_arriendo=100,
            stock=10
        )

    def test_stock_disminuye_arriendo(self):
        pelicula = Pelicula.objects.first()
        pelicula.stock -= 1
        pelicula.save()
        self.assertEqual(pelicula.stock, 9)