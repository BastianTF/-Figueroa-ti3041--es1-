from django.db import models
from django.contrib.auth.models import User


class Venta(models.Model):
	ESTADOS = (
		('pendiente', 'Pendiente'),
		('pagada', 'Pagada'),
		('enviada', 'Enviada'),
		('completada', 'Completada'),
		('cancelada', 'Cancelada'),
	)

	cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas')
	detalle = models.JSONField(default=list)
	total = models.PositiveIntegerField(default=0)
	estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
	creada_en = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-creada_en']

	def __str__(self):
		return f'Venta #{self.pk} - {self.cliente.username}'


class PerfilCliente(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
	cupo = models.PositiveIntegerField(default=100000)

	def __str__(self):
		return f'Perfil de {self.usuario.username}'
