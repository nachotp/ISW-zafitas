from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import *
from .forms import *
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = "base.html"


class ProductView(DetailView):
    model = Producto
    template_name = "verproductos.html"


class SolicitudView(FormView):
    form_class = ProdEnPedidoForm
    template_name = "solicitudes.html"

    def get_context_data(self, **kwargs):
        data = super(SolicitudView, self).get_context_data(**kwargs)
        if self.request.POST:
            datos = ProdEnPedidoFormSet(self.request.POST)
            if datos.is_valid():
                maxforms = int(self.request.POST['form-TOTAL_FORMS'][0])
                obra = int(self.request.POST['form-0-obra'][0])
                pedido = Pedido.objects.create(obra=Obra.objects.get(id=obra),
                                               usuario=self.request.user,
                                               fecha=timezone.now(),
                                               comentario="Funciona!")
                for i in range(maxforms):
                    prod = int(self.request.POST['form-{0}-producto'.format(i)][0])
                    cant = int(self.request.POST['form-{0}-cantidad'.format(i)][0])
                    ProductoEnPedido.objects.create(idPedido=pedido,
                                                    idProducto=Producto.objects.get(id=prod),
                                                    cantidad=cant)
            else:
                print(datos.errors)
            data['productos'] = ProdEnPedidoFormSet()
        else:
            data['productos'] = ProdEnPedidoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        return super(SolicitudView, self).form_valid(form)

class PedidoView(ListView):
    model = Pedido
    template_name = "verpedidos.html"


class DetalleView(DetailView):
    model = ProductoEnPedido
    template_name = "detallepedido.html"


class StockView(ListView):
    model = ProductoEnBodega
    context_object_name = 'productos_en_bodega'
    template_name = "verstock.html"


@method_decorator(login_required, name="dispatch")
class AjaxProductosView(ListView):
    http_method_names = ['get', ]

    def dispatch(self, request, *args, **kwargs):
        return super(AjaxProductosView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Producto.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{'id': p.id,
                 'nombre': p.nombre,
                 'desc': p.descripcion} for p in queryset]
        return JsonResponse(data, status=200, safe=False)


@method_decorator(login_required, name="dispatch")
class AjaxObrasView(ListView):
    http_method_names = ['get', ]

    def dispatch(self, request, *args, **kwargs):
        return super(AjaxObrasView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Obra.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{'id': p.id,
                 'nombre': p.ubicacion} for p in queryset]
        return JsonResponse(data, status=200, safe=False)
