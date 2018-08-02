from django.db import models
from django.contrib.auth.models import User
import datetime


class Producto(models.Model):
    idProducto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=400, verbose_name="Descripción del producto")
    marca = models.CharField(max_length=100, verbose_name="Marca")
    precio = models.IntegerField(verbose_name="Precio")

    def __str__(self):
        return self.nombre + " - " + self.descripcion

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'


class Bodega(models.Model):
    idBodega = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicacion")

    def __str__(self):
        return "Ubicacion: " + self.ubicacion

    class Meta:
        verbose_name = 'bodega'
        verbose_name_plural = 'bodegas'


class ProductoEnBodega(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)

class Cotizacion(models.Model):
    idProducto = models.IntegerField(primary_key=True)
    monto = models.IntegerField(primary_key=True, verbose_name="Monto")
    cantidad = models.IntegerField(primary_key=True, verbose_name="Cantidad")
    fecha = models.DateField(verbose_name="fecha", default=datetime.date.today)

    class Meta:
        verbose_name = 'cotizacion'
        verbose_name_plural = 'cotizaciones'

class Obra(models.Model):
    idOrden = models.IntegerField(primary_key=True)
    ubicacion =  models.CharField(max_length=100, verbose_name="Ubicacion")

    class Meta:
        verbose_name = 'obra'
        verbose_name_plural = 'obras'

class Pedido(models.Model):
    idPedido = models.IntegerField(primary_key=True)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'


class Usuario(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    rut =  models.IntegerField(verbose_name="RUT",primary_key=True)
    password = models.CharField(max_length=20, verbose_name="Password")
    PERSONAL_OBRA = "PO"
    ENCARGADO_COMPRA = "EC"
    BODEGUERO = "BG"
    cargos = ((PERSONAL_OBRA,"Personal de obra"),(ENCARGADO_COMPRA,"Encargado de Compras"),(BODEGUERO,"Bodeguero"))
    cargo = models.CharField(max_length=2,choices=cargos, default=PERSONAL_OBRA ,verbose_name="Cargo")

    def __str__(self):
        return self.nombre + " - " + self.cargo

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
