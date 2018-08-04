from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('solicitud', SolicitudView.as_view(), name="Solicitud"),
    path("verprod/<pk>/", ProductView.as_view(), name="verProducto")
]
