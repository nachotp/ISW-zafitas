from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import *
from .forms import *


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
            data['productos'] = ProdEnPedidoFormSet(self.request.POST)
        else:
            data['productos'] = ProdEnPedidoFormSet()
        return data


class PedidoView(ListView):
    model = Pedido
    template_name = "verpedidos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
