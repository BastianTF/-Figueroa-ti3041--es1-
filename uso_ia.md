# Registro de uso de IA

## Proyecto
Catálogo Online - Ferretería Harcha

## Uso realizado

- Se utilizó un agente de IA como apoyo para diseñar la interfaz del catálogo, incluyendo `base.html`, `lista.html`, estilos CSS responsive y la presentación de las tarjetas de productos.
- Se utilizó IA para generar el listado de 40 productos de ferretería en formato JSON, con los campos `id`, `nombre`, `categoria`, `precio` y `stock`.
- Se utilizó IA para asignar imágenes representativas mediante URLs de `loremflickr` usando palabras clave relacionadas con cada producto, por ejemplo martillo, taladro, cable eléctrico y pintura.
- Se utilizó IA para revisar errores de plantillas, validar rutas y comprobar el proyecto con `python manage.py check`.

## Verificación realizada

- Se comprobó que el archivo JSON contiene 40 registros.
- Se comprobó que cada producto tiene nombre, categoría, precio y stock.
- Se comprobó que el listado se carga desde `catalogo/data/productos.json` en `catalogo/views.py`.
- Se comprobó la vista de detalle por id y el manejo de productos inexistentes mediante `Http404`.
- Se comprobó la herencia de templates desde `base.html`.

## Nota sobre imágenes

Las imágenes se asignaron mediante un servicio de fotografías por palabra clave para representar cada producto. No se copiaron fotografías de catálogos de otras tiendas.
