from django.db import models
from usuario.models import User
from datetime import timedelta, datetime
from django.utils import timezone
# Create your models here.


class Paseador(User):
    descripcion = models.TextField(null=True, blank=False)
    cantidad_mascotas = models.IntegerField(default=1)
    foto_perfil = models.ImageField(upload_to="paseadores", null=True, blank=True)

    class Meta:
        db_table = "paseador"


class HorarioPaseo(models.Model):
    DIA_CHOICES = (
        ("lunes", "Lunes"),
        ("martes", "Martes"),
        ("miercoles", "Miércoles"),
        ("jueves", "Jueves"),
        ("viernes", "Viernes"),
        ("sabado", "Sábado"),
        ("domingo", "Domingo"),
    )
    
    paseador = models.ForeignKey(Paseador, on_delete=models.CASCADE)
    dia = models.CharField(max_length=20, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        hora_inicio_datetime = datetime.combine(datetime.now().date(), self.hora_inicio)
        hora_fin_datetime = hora_inicio_datetime + timedelta(hours=1)
        self.hora_fin = hora_fin_datetime.time()
        super().save(*args, **kwargs)
