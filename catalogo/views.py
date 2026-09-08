import json
import os
import random
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from .models import Venta


def cargar_productos():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'productos.json')
    with open(ruta, encoding='utf-8') as archivo:
        return json.load(archivo)


def preparar_producto(producto):
    """Añade contenido comercial mientras los productos sigan viviendo en JSON."""
    producto = producto.copy()
    producto['descripcion'] = (
        f"El {producto['nombre'].lower()} es una solución práctica y confiable "
        f"para tus proyectos de {producto['categoria'].lower()}."
    )
    producto['caracteristicas'] = [
        f"Categoría: {producto['categoria']}",
        'Producto seleccionado para trabajos domésticos y profesionales',
        f"Disponibilidad inmediata: {producto['stock']} unidades",
    ]
    return producto


def home(request):
    productos = cargar_productos()
    total_productos = len(productos)
    productos_disponibles = sum(1 for producto in productos if producto['stock'] > 0)
    productos_sin_stock = total_productos - productos_disponibles
    random.shuffle(productos)
    categorias = sorted({p['categoria'] for p in productos})
    contexto = {
        'productos': productos,
        'categorias': categorias,
        'total_productos': total_productos,
        'productos_disponibles': productos_disponibles,
        'productos_sin_stock': productos_sin_stock,
    }
    return render(request, 'catalogo/lista.html', contexto)


def detalle(request, producto_id):
    productos = cargar_productos()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto is None:
        raise Http404("Producto no encontrado")
    contexto = {'producto': preparar_producto(producto)}
    return render(request, 'catalogo/detalle.html', contexto)

def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('panel_admin' if request.user.is_staff else 'panel_cliente')
    formulario = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        login(request, formulario.get_user())
        destino = 'panel_admin' if request.user.is_staff else 'panel_cliente'
        return redirect(destino)
    return render(request, 'catalogo/login.html', {'formulario': formulario})


def crear_cuenta(request):
    if request.user.is_authenticated:
        return redirect('home')
    formulario = UserCreationForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save()
        login(request, usuario)
        messages.success(request, 'Tu cuenta fue creada correctamente.')
        return redirect('panel_cliente')
    return render(request, 'catalogo/registro.html', {'formulario': formulario})


def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def obtener_carro(request):
    return request.session.get('carro', {})


def carro(request):
    productos = cargar_productos()
    carro_guardado = obtener_carro(request)
    items = []
    total = 0
    for producto_id, cantidad in carro_guardado.items():
        producto = next((p for p in productos if str(p['id']) == str(producto_id)), None)
        if producto is None:
            continue
        item = preparar_producto(producto)
        item['cantidad'] = cantidad
        item['subtotal'] = producto['precio'] * cantidad
        items.append(item)
        total += item['subtotal']
    return render(request, 'catalogo/carro.html', {'items': items, 'total': total})


def agregar_al_carro(request, producto_id):
    if request.method != 'POST':
        return redirect('detalle', producto_id=producto_id)
    productos = cargar_productos()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto is None:
        raise Http404('Producto no encontrado')
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        cantidad = 1
    if producto['stock'] == 0:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('detalle', producto_id=producto_id)
    cantidad = max(1, min(cantidad, producto['stock']))
    carro_guardado = obtener_carro(request)
    actual = int(carro_guardado.get(str(producto_id), 0))
    carro_guardado[str(producto_id)] = min(actual + cantidad, producto['stock'])
    request.session['carro'] = carro_guardado
    request.session.modified = True
    messages.success(request, f'{producto["nombre"]} fue añadido al carro.')
    return redirect('carro')


@user_passes_test(lambda usuario: usuario.is_staff, login_url='login')
def panel_admin(request):
    productos = cargar_productos()
    ventas = Venta.objects.select_related('cliente').all()
    contexto = {
        'productos': productos,
        'ventas': ventas,
        'total_inventario': len(productos),
        'productos_disponibles': sum(1 for producto in productos if producto['stock'] > 0),
        'ventas_pendientes': ventas.filter(estado='pendiente').count(),
        'total_ventas': sum(venta.total for venta in ventas),
    }
    return render(request, 'catalogo/panel_admin.html', contexto)


@login_required(login_url='login')
def panel_cliente(request):
    ventas = request.user.ventas.all()
    return render(request, 'catalogo/panel_cliente.html', {'ventas': ventas})