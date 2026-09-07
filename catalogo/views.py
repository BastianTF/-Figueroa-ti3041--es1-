import json
import os
import random
from django.conf import settings
from django.http import Http404
from django.shortcuts import render


def cargar_productos():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'productos.json')
    with open(ruta, encoding='utf-8') as archivo:
        return json.load(archivo)


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
    contexto = {
        'producto': producto,
    }
    return render(request, 'catalogo/detalle.html', contexto)