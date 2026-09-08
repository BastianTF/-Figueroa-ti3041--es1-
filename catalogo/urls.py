from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('producto/<int:producto_id>/', views.detalle, name='detalle'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.crear_cuenta, name='registro'),
    path('recuperar-clave/', auth_views.PasswordResetView.as_view(
        template_name='catalogo/password_reset_form.html',
        email_template_name='catalogo/password_reset_email.txt',
        subject_template_name='catalogo/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),
    path('recuperar-clave/enviada/', auth_views.PasswordResetDoneView.as_view(
        template_name='catalogo/password_reset_done.html',
    ), name='password_reset_done'),
    path('recuperar-clave/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='catalogo/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete'),
    ), name='password_reset_confirm'),
    path('recuperar-clave/completada/', auth_views.PasswordResetCompleteView.as_view(
        template_name='catalogo/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('panel/administrador/', views.panel_admin, name='panel_admin'),
    path('panel/cliente/', views.panel_cliente, name='panel_cliente'),
        path('carro/', views.carro, name='carro'),
        path('carro/agregar/<int:producto_id>/', views.agregar_al_carro, name='agregar_al_carro'),
        path('carro/eliminar/<int:producto_id>/', views.eliminar_del_carro, name='eliminar_del_carro'),
        path('carro/finalizar/', views.finalizar_compra, name='finalizar_compra'),
        path('panel/administrador/stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
]