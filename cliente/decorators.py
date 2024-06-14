from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mascota, Cliente
from django.core.exceptions import ObjectDoesNotExist


def verificar_usuario_cliente(function):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name="cliente").exists():
            return function(request, *args, **kwargs)
        else:
            return redirect(to="index")
        raise Http404

    return wrapper


def verificar_cliente_mascota(function):
    def wrapper(request, id, *args, **kwargs):
        try:
            mascota = Mascota.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("La mascota no existe.")
        cliente = mascota.duenno

        # Verificar si el usuario actual es el propietario del cliente
        if cliente != request.user.cliente:
            return HttpResponseForbidden(
                "No tienes permiso para acceder a esta mascota."
            )
        return function(request, id, *args, **kwargs)

    return wrapper
