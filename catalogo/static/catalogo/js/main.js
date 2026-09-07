document.addEventListener('DOMContentLoaded', function () {
    const buscador = document.getElementById('buscador');
    const filtroCategoria = document.getElementById('filtro-categoria');
    const filtroPrecio = document.getElementById('filtro-precio');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const tarjetas = document.querySelectorAll('.card-producto');

    function aplicarFiltros() {
        const texto = buscador.value.toLowerCase();
        const categoria = filtroCategoria.value;
        const rangoPrecio = filtroPrecio.value;

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

    if (buscador) buscador.addEventListener('input', aplicarFiltros);
    if (filtroCategoria) filtroCategoria.addEventListener('change', aplicarFiltros);
    if (filtroPrecio) filtroPrecio.addEventListener('change', aplicarFiltros);

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', function () {
            buscador.value = '';
            filtroCategoria.value = '';
            filtroPrecio.value = '';
            aplicarFiltros();
        });
    }

    // --- Modal de login (solo visual, sin autenticación real) ---
    const btnLogin = document.getElementById('btn-login');
    const modalLogin = document.getElementById('modal-login');
    const cerrarModal = document.getElementById('cerrar-modal');

    if (btnLogin && modalLogin) {
        btnLogin.addEventListener('click', function () {
            modalLogin.classList.add('activo');
        });
        cerrarModal.addEventListener('click', function () {
            modalLogin.classList.remove('activo');
        });
        modalLogin.addEventListener('click', function (e) {
            if (e.target === modalLogin) modalLogin.classList.remove('activo');
        });
    }
});