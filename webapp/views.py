from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView, FormView,CreateView
from .models import *
from .forms import *
from .odooapi import OdooAPI


@method_decorator(login_required, name="dispatch")
class IndexView(TemplateView):
    template_name = "base.html"


class CruzarPedidoView(TemplateView):
    model = Pedido
    template_name = "cruzarstock.html"

    def get_context_data(self, **kwargs):
        context = super(CruzarPedidoView, self).get_context_data(**kwargs)
        context['object'] = Pedido.objects.get(id=self.kwargs['pk'])
        prodenpedidos = ProductoEnPedido.objects.filter(idPedido=context['object'].id)
        stock = []
        for pep in prodenpedidos:
            name = pep.idProducto.nombre
            enstock = ProductoEnBodega.objects.get(idProducto=pep.idProducto).cantidad
            cant = enstock - pep.cantidad
            falta = 1 if cant < 0 else 0
            stock.append((pep.idProducto.id, name, pep.cantidad, enstock, abs(cant), falta))
        context['stock'] = stock

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        data = self.request.POST
        cantprods = int(len(data)/2)
        requestlist = []
        for i in range(cantprods):
            requestlist.append({'id': int(data['prodid-'+str(i+1)]),
                                'name': Producto.objects.get(pk=data['prodid-'+str(i+1)]).nombre,
                                'cantidad': int(data['prodcant-'+str(i+1)])
                                })
        print(requestlist)
        # MONSE
        # HAS
        # TU
        # MAGIA
        # ACA
        # 💕❤😘
        return super(TemplateView, self).render_to_response(context)

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
                maxforms = int(self.request.POST['form-TOTAL_FORMS'])
                obra = int(self.request.POST['form-0-obra'])
                comentario = self.request.POST['comentario']
                pedido = Pedido.objects.create(obra=Obra.objects.get(id=obra),
                                               usuario=self.request.user,
                                               fecha=timezone.now(),
                                               comentario=comentario)
                for i in range(maxforms):
                    prod = int(self.request.POST['form-{0}-producto'.format(i)])
                    cant = int(self.request.POST['form-{0}-cantidad'.format(i)])
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


class RegistroView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registro.html'

    def get_context_data(self, **kwargs):
        context = super(RegistroView, self).get_context_data(**kwargs)
        context['cargos'] = Perfil.cargos
        return context


class DetallePedidoView(DetailView):
    model = Pedido
    template_name = "detallepedido.html"

    def get_context_data(self, **kwargs):
        context = super(DetallePedidoView, self).get_context_data(**kwargs)
        context['prodenpedidos'] = ProductoEnPedido.objects.filter(idPedido=context['object'].id)
        return context


class StockView(ListView):
    model = ProductoEnBodega
    context_object_name = 'productos_en_bodega'
    template_name = "verstock.html"


class CotizacionView(TemplateView):
    url, db, username, password = 'https://gpi-isw.odoo.com', 'gpi-isw', 'isw.zafitas@gmail.com', 'iswgpi123'
    template_name = 'cotizacion.html'
    api = OdooAPI(url, db, username, password)

    def get_context_data(self, **kwargs):

        data = self.api.search_read('purchase.order', [], ['partner_id','state','amount_total','date_order','notes','order_line'])
        data2 = self.api.search_read('purchase.order.line', [],['name'])
        context = {'data': data}
        print(data2)
        self.api.getInfo()
        return context


class DetalleCotizacionView(TemplateView):
    url, db, username, password = 'https://gpi-isw.odoo.com', 'gpi-isw', 'isw.zafitas@gmail.com', 'iswgpi123'
    template_name = 'detallecotizacion.html'
    api = OdooAPI(url, db, username, password)

    def get_context_data(self, **kwargs):
        class_id = self.kwargs['id_c']
        data = self.api.search_read('purchase.order', [], ['partner_id','state','amount_total','date_order','notes','order_line'])
        data2 = self.api.search_read('purchase.order.line', [], ['product_id','name','price_subtotal','price_unit','product_qty'])
        context = {'data': data, 'linea': data2,'idd':int(class_id)}
        print(context)
        return context


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
