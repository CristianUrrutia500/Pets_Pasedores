from django.db import models
from usuario.models import User

# Create your models here.


class Cliente(User):
    class Meta:
        db_table = "cliente"


class Mascota(models.Model):
    TAMANNO_CHOICES = [
        ("pequenno", "Pequeño"),
        ("mediano", "Mediano"),
        ("grande", "Grande"),
    ]
    duenno = models.ForeignKey(
        Cliente, verbose_name=("dueño"), on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=30)
    edad = models.IntegerField()
    foto = models.ImageField(upload_to="mascotas", null=True, blank=True)
    tamanno = models.CharField(
        max_length=20, choices=TAMANNO_CHOICES, default="pequenno", blank=False
    )

    def __str__(self) -> str:
        return f"{self.nombre}"
