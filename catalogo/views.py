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


def dividir_en_columnas(productos, n_columnas=3):
    columnas = [[] for _ in range(n_columnas)]
    for i, producto in enumerate(productos):
        columnas[i % n_columnas].append(producto)
    return columnas


def home(request):
    productos = cargar_productos()
    random.shuffle(productos)
    categorias = sorted({p['categoria'] for p in productos})
    contexto = {
        'columnas': dividir_en_columnas(productos, 3),
        'categorias': categorias,
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