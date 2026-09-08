from django.contrib import admin
from .models import Venta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
	list_display = ('id', 'cliente', 'total', 'estado', 'creada_en')
	list_filter = ('estado', 'creada_en')
	search_fields = ('cliente__username', 'cliente__email')
	readonly_fields = ('creada_en',)
