from django.urls import path, include, re_path
from django.contrib import admin
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('solicitud', SolicitudView.as_view(), name="Solicitud"),
    path("verprod/<pk>/", ProductView.as_view(), name="verProducto"),
    path("stock", StockView.as_view(), name='verStock'),
    path('pedidos', PedidoView.as_view(), name='verPedidos'),
    path('detalle/<pk>', DetallePedidoView.as_view(), name='DetallePedido'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("cotizaciones",CotizacionView.as_view(), name="verCotizacion"),
    re_path(r'^dtc/(?P<id_c>\d+)/$', DetalleCotizacionView.as_view(), name="DetalleCotizacion"),
    path('cruzarpedido/<pk>/', CruzarPedidoView.as_view(), name="cruzarstock"),
    path('registro/', RegistroView.as_view(), name='Registro')
]
# API URLS
urlpatterns += [
    path("api/getprods", AjaxProductosView.as_view()),
    path("api/getobras", AjaxObrasView.as_view())]