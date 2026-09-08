from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('producto/<int:producto_id>/', views.detalle, name='detalle'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.crear_cuenta, name='registro'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('panel/administrador/', views.panel_admin, name='panel_admin'),
    path('panel/cliente/', views.panel_cliente, name='panel_cliente'),
        path('carro/', views.carro, name='carro'),
        path('carro/agregar/<int:producto_id>/', views.agregar_al_carro, name='agregar_al_carro'),
        path('carro/finalizar/', views.finalizar_compra, name='finalizar_compra'),
        path('panel/administrador/stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
]