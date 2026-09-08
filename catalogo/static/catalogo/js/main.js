document.addEventListener('DOMContentLoaded', function () {
    const buscador = document.getElementById('buscador');
    const filtroCategoria = document.getElementById('filtro-categoria');
    const filtroPrecio = document.getElementById('filtro-precio');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const ordenarPor = document.getElementById('ordenar-por');
    const grid = document.getElementById('tabla-productos');
    const tarjetas = Array.from(document.querySelectorAll('.card-producto'));

    function aplicarFiltros() {
        const texto = buscador ? buscador.value.toLowerCase() : '';
        const categoria = filtroCategoria ? filtroCategoria.value : '';
        const rangoPrecio = filtroPrecio ? filtroPrecio.value : '';

        let min = null, max = null;
        if (rangoPrecio) {
            const partes = rangoPrecio.split('-');
            min = parseInt(partes[0], 10);
            max = parseInt(partes[1], 10);
        }

        tarjetas.forEach(function (tarjeta) {
            const nombre = tarjeta.dataset.nombre;
            const cat = tarjeta.dataset.categoria;
            const precio = parseInt(tarjeta.dataset.precio, 10);

            let visible = true;
            if (texto && !nombre.includes(texto)) visible = false;
            if (categoria && cat !== categoria) visible = false;
            if (min !== null && (precio < min || precio > max)) visible = false;

            tarjeta.style.display = visible ? '' : 'none';
        });
    }

    function aplicarOrden() {
        if (!ordenarPor || !grid) return;
        const criterio = ordenarPor.value;
        let ordenadas = tarjetas.slice();

        if (criterio === 'precio-asc') {
            ordenadas.sort((a, b) => parseInt(a.dataset.precio) - parseInt(b.dataset.precio));
        } else if (criterio === 'precio-desc') {
            ordenadas.sort((a, b) => parseInt(b.dataset.precio) - parseInt(a.dataset.precio));
        } else if (criterio === 'nombre-asc') {
            ordenadas.sort((a, b) => a.dataset.nombre.localeCompare(b.dataset.nombre));
        }

        ordenadas.forEach(function (tarjeta) {
            grid.appendChild(tarjeta);
        });
    }

    if (buscador) buscador.addEventListener('input', aplicarFiltros);
    if (filtroCategoria) filtroCategoria.addEventListener('change', aplicarFiltros);
    if (filtroPrecio) filtroPrecio.addEventListener('change', aplicarFiltros);
    if (ordenarPor) ordenarPor.addEventListener('change', aplicarOrden);

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', function () {
            if (buscador) buscador.value = '';
            if (filtroCategoria) filtroCategoria.value = '';
            if (filtroPrecio) filtroPrecio.value = '';
            aplicarFiltros();
        });
    }

});