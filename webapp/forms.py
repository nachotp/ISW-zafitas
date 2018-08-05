import django.forms as forms


class ProdEnPedidoForm(forms.Form):
    producto = forms.ChoiceField(choices=(), label="Producto")
    cantidad = forms.IntegerField(label="Cantidad", min_value=1)
    obra = forms.IntegerField(min_value=0)


ProdEnPedidoFormSet = forms.formset_factory(ProdEnPedidoForm, can_delete=True)


