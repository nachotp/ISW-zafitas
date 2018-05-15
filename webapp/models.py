from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=400, verbose_name="Descripción del producto")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    precio = models.IntegerField(verbose_name="Precio")

    def __str__(self):
        return self.nombre + " - " + self.descripcion

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
