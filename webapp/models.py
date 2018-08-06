from django.db import models
from django.contrib.auth.models import User
import datetime


class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
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
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicacion")

    def __str__(self):
        return "Ubicacion: " + self.ubicacion

    class Meta:
        verbose_name = 'bodega'
        verbose_name_plural = 'bodegas'


class ProductoEnBodega(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)


'''
class Cotizacion(models.Model):
    idProducto = models.IntegerField(primary_key=True)
    monto = models.IntegerField(verbose_name="Monto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateField(verbose_name="fecha", default=datetime.date.today)

    class Meta:
        verbose_name = 'cotizacion'
        verbose_name_plural = 'cotizaciones'
'''


class Obra(models.Model):
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicacion")

    class Meta:
        verbose_name = 'obra'
        verbose_name_plural = 'obras'


class Pedido(models.Model):
    obra = models.ForeignKey(Obra, verbose_name="Obra", on_delete=models.CASCADE)
    comentario = models.CharField(max_length=300, verbose_name='Comentario')
    fecha = models.DateField(verbose_name="fecha", default=datetime.date.today)
    ING = "Ingresado"
    ET = "En Transito"
    EB = "En Bodega"
    EP = "Esperando Proveedor"
    RR = "Rechazado"
    FF = "Entregado"
    estados = ((ING, "Ingresado"), (ET, "En Transito"), (EB, "En Bodega"), (EP, "Esperando Proveedor"), (RR, "Rechazado"), (FF, "Entregado"))
    estado = models.CharField(max_length=20, choices=estados, default=ING, verbose_name="Estado")

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return "Pedido #"+str(self.id) + " " + self.obra.ubicacion


class ProductoEnPedido(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Producto en pedido'
        verbose_name_plural = 'Productos en Pedidos'

    def __str__(self):
        return str(self.cantidad) + " " + self.idProducto.nombre + " | " + str(self.idPedido)


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    rut = models.IntegerField(verbose_name="RUT")
    PERSONAL_OBRA = "PO"
    ENCARGADO_COMPRA = "EC"
    BODEGUERO = "BG"
    cargos = ((PERSONAL_OBRA, "Personal de obra"), (ENCARGADO_COMPRA, "Encargado de Compras"), (BODEGUERO, "Bodeguero"))
    cargo = models.CharField(max_length=2, choices=cargos, default=PERSONAL_OBRA, verbose_name="Cargo")

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return self.nombre + " - " + self.cargo

    '''
    @receiver(post_save, sender=User)
    def crear_perfil(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(usuario=instance)

    @receiver(post_save, sender=User)
    def guardar_perfil(sender, instance, **kwargs):
        instance.profile.save()
    '''
