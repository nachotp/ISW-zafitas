from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView
from .models import *


class IndexView(TemplateView):
    template_name = "base.html"


class ProductView(DetailView):
    model = Producto
    template_name = "verproductos.html"
