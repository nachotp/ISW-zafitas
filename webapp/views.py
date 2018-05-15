from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import *


class IndexView(TemplateView):
    template_name = "index.html"
