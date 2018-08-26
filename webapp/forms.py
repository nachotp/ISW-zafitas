import django.forms as forms
from django.db import models
from django.contrib.auth.models import User

class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class ProdEnPedidoForm(forms.Form):
    producto = ChoiceFieldNoValidation(choices=(), label="Producto")
    cantidad = forms.IntegerField(label="Cantidad", min_value=1)
    obra = forms.IntegerField(min_value=0)

class UserRegistrationForm(forms.Form):
    PERSONAL_OBRA = "PO"
    ENCARGADO_COMPRA = "EC"
    BODEGUERO = "BG"
    cargos = ((PERSONAL_OBRA, "Personal de obra"), (ENCARGADO_COMPRA, "Encargado de Compras"), (BODEGUERO, "Bodeguero"))
    cargo = models.CharField(max_length=2, choices=cargos, default=PERSONAL_OBRA, verbose_name="Cargo")
    rut = forms.IntegerField(
        required = True,
        label = 'Rut',
    )
    nombre = forms.CharField(
        required=True,
        label='Nombre',
        max_length=32
    )
    cargo= forms.ChoiceField(choices=cargos, label='Cargo')
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','password','nombre','rut','cargo')

ProdEnPedidoFormSet = forms.formset_factory(ProdEnPedidoForm, can_delete=True)
UserRegistrationFormSet = forms.formset_factory(UserRegistrationForm, can_delete=True)

