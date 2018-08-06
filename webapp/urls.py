from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('solicitud', SolicitudView.as_view(), name="Solicitud"),
    path("verprod/<pk>/", ProductView.as_view(), name="verProducto"),
    path("stock", StockView.as_view(), name='verStock'),
    path('pedidos', PedidoView.as_view(), name='verPedidos'),
    path('detalle/<pk>', DetalleView.as_view(), name='DetallePedido')
]

# API URLS
urlpatterns += [
    path("api/getprods", AjaxProductosView.as_view()),
    path("api/getobras", AjaxObrasView.as_view())]