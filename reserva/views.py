from django.shortcuts import render,redirect, get_object_or_404
from cliente.decorators import verificar_usuario_cliente, verificar_cliente_mascota
from .forms import ReservaForm, Reserva
from django.contrib import messages
from paseador.models import HorarioPaseo
from datetime import datetime
from cliente.models import Cliente
from paseador.models import Paseador, HorarioPaseo
from paseador.decorators import verificar_usuario_paseador
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

@verificar_usuario_cliente
def reservar_paseo(request, horario_paseo_id):
    horario = get_object_or_404(HorarioPaseo, pk=horario_paseo_id)
    horarios_disponibles = HorarioPaseo.objects.filter(paseador=horario.paseador)
    if request.method == 'POST':
        form = ReservaForm(request.user, horarios_disponibles=horarios_disponibles, data=request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            mascotas_seleccionadas = form.cleaned_data['mascotas']

            # reserva.horario_paseo = horario
            horario_paseo = form.cleaned_data['horario_paseo']
            fecha_paseo = form.cleaned_data['fecha_paseo']

            # Verificar si se ha alcanzado el límite máximo de mascotas
            cantidad_reservas = Reserva.objects.filter(horario_paseo=horario_paseo, fecha_paseo=fecha_paseo).count()
            if cantidad_reservas + len(mascotas_seleccionadas) > horario_paseo.paseador.cantidad_mascotas:
                messages.info(request, "Se ha alcanzado el máximo de mascotas para este paseo.")
                return redirect(to="cliente:info-paseador",paseador_id = horario.paseador.id)
            
            # Verificar si la fecha de paseo es anterior al día actual
            if fecha_paseo < datetime.now().date():
                messages.error(request, "La fecha de paseo no puede ser inferior a la fecha actual.")
                return redirect(to="cliente:info-paseador",paseador_id = horario.paseador.id)
            
            # Si la fecha de paseo es igual al día actual, comprobar la hora
            if fecha_paseo == datetime.now().date() and horario_paseo.hora_inicio < datetime.now().time():
                messages.error(request, "No puedes reservar un horario en el pasado.")
                return redirect(to="cliente:info-paseador",paseador_id = horario.paseador.id)
            
            # Verificar si la fecha de paseo coincide con el día del horario de paseo
            # Convertir horario_paseo.dia a número de día de la semana
            dias_semana = {
                'lunes': 0,
                'martes': 1,
                'miercoles': 2,
                'jueves': 3,
                'viernes': 4,
                'sabado': 5,
                'domingo': 6
            }
            dia_semana_horario_paseo = dias_semana[horario_paseo.dia.lower()]

            if fecha_paseo.weekday() != dia_semana_horario_paseo:
                messages.error(request, "La fecha de paseo debe coincidir con el día del horario de paseo del paseador.")
                return redirect(to="cliente:info-paseador",paseador_id = horario.paseador.id)
            
            for mascota in mascotas_seleccionadas:
                #calcular precio por mascota dependiendo el tamanno
                if mascota.tamanno in ('pequenno','mediano'):
                    precio = 8000
                else:
                    precio = 10000
                # Crear una instancia de Reserva para cada mascota
                reserva = Reserva(mascota=mascota, horario_paseo=horario_paseo, fecha_paseo= fecha_paseo, precio = precio)
                reserva.save()
            
            messages.success(request, "Reserva correctamente.")

            return redirect(to="lista-reservas")
    else:
        form = ReservaForm(request.user, horarios_disponibles=horarios_disponibles, initial={'horario_paseo': horario})
    
    data = {
        "form": form,
        "horario":horario,
    }
    return render(request, "cliente/paseo/registrar_reserva.html", data)

@verificar_usuario_cliente
def listar_reservas(request):
    cliente = Cliente.objects.get(pk=request.user.id)
    reservas_cliente = Reserva.objects.filter(mascota__duenno=cliente)
    reservas_cliente = Reserva.objects.filter(mascota__duenno=cliente).order_by('fecha_paseo','horario_paseo__dia', 'horario_paseo__hora_inicio')
    data ={
        'reservas_cliente':reservas_cliente,
    }
    return render(request,'cliente/paseo/lista_reservas.html', data)

@verificar_usuario_paseador
def listar_reservas_paseador(request):
    paseador = Paseador.objects.get(pk=request.user.id)
    reservas_paseador = Reserva.objects.filter(horario_paseo__paseador=paseador)

    reservas_paseador = reservas_paseador.order_by('fecha_paseo','horario_paseo__dia', 'horario_paseo__hora_inicio')
    data = {
        'reservas_paseador':reservas_paseador,
    }
    return render(request, 'paseador/reservas/lista_reservas_pas.html', data)

@verificar_usuario_paseador
def detalles_solicitud(request, reserva_id):
    reserva = Reserva.objects.get(pk=reserva_id)
    data = {
        'reserva':reserva,
    }
    return render(request, 'paseador/reservas/detalles_sol_reserva.html', data)

@verificar_usuario_paseador
def rechazar_solicitud(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    # Marcar la reserva como rechazada
    reserva.estado = 'rechazada'
    reserva.save()
    # Envío de correo electrónico al cliente
    subject = 'Reserva rechazada'
    message = f'''
    Hola {reserva.mascota.duenno.first_name},

    Lamentamos informarte que tu reserva ha sido rechazada.

    Detalles de la reserva:
    - Mascota: {reserva.mascota.nombre}
    - Fecha de Paseo: {reserva.fecha_paseo.strftime("%Y-%m-%d")}
    - Día: {reserva.horario_paseo.dia}
    - Hora de Inicio: {reserva.horario_paseo.hora_inicio.strftime("%H:%M")}
    - Paseador: {reserva.horario_paseo.paseador.first_name} {reserva.horario_paseo.paseador.last_name}

    Por favor, contacta con nosotros para más detalles.

    '''
    from_email = settings.EMAIL_HOST_USER
    to_email = reserva.mascota.duenno.email
    send_mail(subject, message, from_email, [to_email])
    messages.error(request, "Reserva rechazada")
    return redirect(to='lista-reservas-paseador')

@verificar_usuario_paseador
def aceptar_solicitud(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    # Marcar la reserva como aceptada
    reserva.estado = 'aceptada'
    reserva.save()
    # Envío de correo electrónico al cliente
    subject = '¡Reserva aceptada!'
    message = f'''
    ¡Hola {reserva.mascota.duenno.first_name}!

    Tu reserva para {reserva.mascota.nombre} ha sido aceptada.
    
    Detalles de la reserva:
    - Mascota: {reserva.mascota.nombre}
    - Fecha de Paseo: {reserva.fecha_paseo.strftime("%Y-%m-%d")}
    - Día: {reserva.horario_paseo.dia}
    - Hora de Inicio: {reserva.horario_paseo.hora_inicio.strftime("%H:%M")}
    - Paseador: {reserva.horario_paseo.paseador.first_name} {reserva.horario_paseo.paseador.last_name}
    - Número de Contacto: {reserva.horario_paseo.paseador.telefono}

    ¡Esperamos verte pronto!
    '''
    from_email = settings.EMAIL_HOST_USER
    to_email = reserva.mascota.duenno.email
    send_mail(subject, message, from_email, [to_email])

    messages.success(request, "Reserva aceptada")
    return redirect(to='lista-reservas-paseador')

@verificar_usuario_cliente
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    # reserva.estado = 'rechazada'
    reserva.delete()
    messages.info(request, "Reserva Cancelada correctamente.")
    return redirect(to="lista-reservas")

@verificar_usuario_paseador
def cancelar_reserva_pas(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    # reserva.estado = 'rechazada'
    reserva.delete()
    messages.info(request, "Reserva Cancelada correctamente.")
    return redirect(to="lista-reservas-paseador")