from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path("verprod/<pk>/", ProductView.as_view(), name="verProducto")
]
