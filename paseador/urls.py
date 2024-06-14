from django.urls import path
from .views import (
    registro_paseador,
    interfaz_paseador,
    listar_horario,
    registrar_horario_paseo,
    perfil_paseador,
    modificar_horario,
    eliminar_horario,
    update_profile
)

urlpatterns = [
    path("registro-paseador/", registro_paseador, name="registro-paseador"),
    path("interfaz-paseador/", interfaz_paseador, name="interfaz-paseador"),
    path("listar-horario/", listar_horario, name="listar-horario"),
    path("registrar-horario/", registrar_horario_paseo, name="registrar-horario"),
    path("perfil-paseador/", perfil_paseador, name="perfil-paseador"),
    path("modificar-horario/<id>", modificar_horario, name="modificar-horario"),
    path("eliminar-horario/<id>", eliminar_horario, name="eliminar-horario"),
    path('update-profile/', update_profile, name='update_profile'),
]
