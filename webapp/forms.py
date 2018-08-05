import django.forms as forms
from .models import *


class ProdEnPedido(forms.Form):
    producto = forms.ChoiceField(choices=(), label="Producto")
    cantidad = forms.IntegerField(label="Cantidad", min_value=1)


