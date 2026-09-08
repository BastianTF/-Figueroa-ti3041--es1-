def carro(request):
    contenido = request.session.get('carro', {})
    cantidad = sum(int(valor) for valor in contenido.values())
    return {'cantidad_carro': cantidad}
