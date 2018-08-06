import django.forms as forms


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class ProdEnPedidoForm(forms.Form):
    producto = ChoiceFieldNoValidation(choices=(), label="Producto")
    cantidad = forms.IntegerField(label="Cantidad", min_value=1)
    obra = forms.IntegerField(min_value=0)


ProdEnPedidoFormSet = forms.formset_factory(ProdEnPedidoForm, can_delete=True)
