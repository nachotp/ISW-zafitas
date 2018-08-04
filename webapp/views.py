from django.views.generic import TemplateView, DetailView
from .models import *


class IndexView(TemplateView):
    template_name = "base.html"


class ProductView(DetailView):
    model = Producto
    template_name = "verproductos.html"


class SolicitudView(TemplateView):
    template_name = "solicitudes.html"

