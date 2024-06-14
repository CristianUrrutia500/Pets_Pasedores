from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    COMUNAS_CHOICES = (
        ("Cerrillos", "Cerrillos"),
        ("Cerro Navia", "Cerro Navia"),
        ("Conchalí", "Conchalí"),
        ("El Bosque", "El Bosque"),
        ("Estación Central", "Estación Central"),
        ("Huechuraba", "Huechuraba"),
        ("Independencia", "Independencia"),
        ("La Cisterna", "La Cisterna"),
        ("La Florida", "La Florida"),
        ("La Granja", "La Granja"),
        ("La Pintana", "La Pintana"),
        ("La Reina", "La Reina"),
        ("Las Condes", "Las Condes"),
        ("Lo Barnechea", "Lo Barnechea"),
        ("Lo Espejo", "Lo Espejo"),
        ("Lo Prado", "Lo Prado"),
        ("Macul", "Macul"),
        ("Maipú", "Maipú"),
        ("Ñuñoa", "Ñuñoa"),
        ("Padre Hurtado", "Padre Hurtado"),
        ("Pedro Aguirre Cerda", "Pedro Aguirre Cerda"),
        ("Peñalolén", "Peñalolén"),
        ("Providencia", "Providencia"),
        ("Pudahuel", "Pudahuel"),
        ("Puente Alto", "Puente Alto"),
        ("Quilicura", "Quilicura"),
        ("Quinta Normal", "Quinta Normal"),
        ("Recoleta", "Recoleta"),
        ("Renca", "Renca"),
        ("San Bernardo", "San Bernardo"),
        ("San Joaquín", "San Joaquín"),
        ("San José de Maipo", "San José de Maipo"),
        ("San Miguel", "San Miguel"),
        ("San Ramón", "San Ramón"),
        ("Santiago", "Santiago"),
        ("Talagante", "Talagante"),
        ("Tiltil", "Tiltil"),
        ("Vitacura", "Vitacura"),
    )
    email = models.EmailField(unique=True,blank=False)
    edad = models.IntegerField(blank=False, null=True)
    direccion = models.CharField(max_length=80, blank=False, null=True)
    telefono = models.CharField(max_length=20, blank=False, null=True)
    comuna = models.CharField(
        max_length=100, choices=COMUNAS_CHOICES, null=True, blank=False
    )

    class Meta:
        db_table = "auth_user"
