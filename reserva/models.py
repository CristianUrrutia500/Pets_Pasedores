from django.db import models
from cliente.models import Mascota
from paseador.models import HorarioPaseo
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib import messages

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('rechazada', 'Rechazada'),
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE,null=True)
    horario_paseo = models.ForeignKey(HorarioPaseo, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_paseo = models.DateField(null=True, blank=False)
    precio = models.IntegerField(null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Reserva de {self.mascota} con {self.horario_paseo.paseador} el {self.horario_paseo.dia} a las {self.horario_paseo.hora_inicio}, {self.fecha_paseo}, precio:{self.precio} Estado:{self.estado}"

# @receiver(pre_save, sender=Reserva)
# def verificar_max_mascotas_por_paseo(sender, instance, **kwargs):
#     horario_paseo = instance.horario_paseo
#     cantidad_reservas = Reserva.objects.filter(horario_paseo=horario_paseo).count()
#     if cantidad_reservas >= horario_paseo.paseador.cantidad_mascotas:
#         raise ValidationError("Se ha alcanzado el máximo de mascotas para este paseo")