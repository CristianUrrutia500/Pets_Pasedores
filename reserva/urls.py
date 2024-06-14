from django.urls import path
from .views import (
    reservar_paseo,
    listar_reservas,
    listar_reservas_paseador,
    detalles_solicitud,
    rechazar_solicitud,
    aceptar_solicitud,
    cancelar_reserva,
    cancelar_reserva_pas
)

urlpatterns = [
    path("registro-reserva/<horario_paseo_id>/", reservar_paseo, name="registro-reserva"),
    path("lista-reservas/", listar_reservas, name="lista-reservas"),
    path("lista-reservas-paseador/",listar_reservas_paseador,name="lista-reservas-paseador",),
    path("solicitud-reserva/<reserva_id>", detalles_solicitud, name="solicitud-reserva"),
    path('rechazar-reserva/<int:reserva_id>/', rechazar_solicitud, name='rechazar-reserva'),
    path('aceptar-reserva/<int:reserva_id>/', aceptar_solicitud, name='aceptar-reserva'),
    path('cancelar-reserva/<int:reserva_id>/', cancelar_reserva, name='cancelar-reserva'),
    path('cancelar-reserva-paseador/<int:reserva_id>/', cancelar_reserva_pas, name='cancelar-reserva-paseador'),
]
