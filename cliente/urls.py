from django.urls import path
from . import views
from .views import (
    registro_cliente,
    interfaz_cliente,
    listar_mascotas,
    registrar_mascota,
    modificar_mascota,
    eliminar_mascota,
    listar_paseadores,
    perfil_cliente,
    info_paseador, 
    verify_email,
    update_profile 
    )

urlpatterns = [
    path("registro-cliente/", registro_cliente, name="registro-cliente"),
    path("interfaz-cliente/", interfaz_cliente, name="interfaz-cliente"),
    path("lista-mascotas/", listar_mascotas, name="lista-mascotas"),
    path("registrar-mascotas/", registrar_mascota, name="registrar-mascotas"),
    path("modificar-mascota/<id>", modificar_mascota, name="modificar-mascota"),
    path("eliminar-mascota/<id>", eliminar_mascota, name="eliminar-mascota"),
    path('lista-paseadores/', listar_paseadores, name="lista-paseadores"),
    path('perfil-cliente/', perfil_cliente, name="perfil-cliente"),
    path('info-paseador/<int:paseador_id>', info_paseador, name="info-paseador"),
    path("verify-email/<str:uidb64>/<str:token>/", verify_email, name="verify_email"),
    path('update-profile/', update_profile, name='update_profile'),
]

