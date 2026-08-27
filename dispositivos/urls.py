from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('zonas/')), # Si entra a la raíz, redirige a /zonas/
    path('zonas/', views.listado_zonas, name='listado_zonas'),
    path('zonas/<int:zona_id>/', views.detalle_zona, name='detalle_zona'),
]