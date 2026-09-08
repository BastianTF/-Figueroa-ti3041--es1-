from django import template

register = template.Library()


@register.filter
def miles(valor):
    """Formatea enteros con punto como separador de miles."""
    try:
        return f'{int(valor):,}'.replace(',', '.')
    except (TypeError, ValueError):
        return valor
