from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView
from .models import *


class IndexView(TemplateView):
    template_name = "base.html"


class ProductView(DetailView):
    model = Producto
    template_name = "verproductos.html"


class SolicitudView(TemplateView):
    template_name = "solicitudes.html"


class PedidoView(TemplateView):
    template_name = "verpedidos.html"


class StockView(ListView):
    model= ProductoEnBodega
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
