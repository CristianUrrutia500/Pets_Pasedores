from datetime import timedelta, datetime
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PaseadorCreationForm, Paseador, HorarioPaseoForm, HorarioPaseo, PaseadorUpdateForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from .decorators import verificar_usuario_paseador, verificar_paseeador_horario
from django.contrib import messages
from reserva.models import Reserva

# Create your views here.


def registro_paseador(request):
    opciones = Paseador.COMUNAS_CHOICES
    data = {"form": PaseadorCreationForm(), "opciones": opciones}
    if request.method == "POST":
        formulario = PaseadorCreationForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            # Guardar el formulario y obtener el usuario registrado
            usuario_registrado = formulario.save()
            # Obtener el grupo 'paseador'
            grupo = Group.objects.get(name="paseador")
            # Agregar el usuario al grupo
            grupo.user_set.add(usuario_registrado)
            # Para autenticar y logear
            usuario_login = authenticate(
                username=formulario.cleaned_data["username"],
                password=formulario.cleaned_data["password1"],
            )
            login(request, usuario_login)
            messages.success(request, "Registrado correctamente.")
            return redirect(to="paseador:interfaz-paseador")
        else:
            data["form"] = formulario

    return render(request, "registration/registro_paseadores.html", data)




@verificar_usuario_paseador
def perfil_paseador(request):
    paseador = Paseador.objects.get(pk=request.user.id)
    data = {"paseador": paseador}
    return render(request, "paseador/perfil/perfil.html", data)


@verificar_usuario_paseador
def interfaz_paseador(request):
    paseador = Paseador.objects.get(pk=request.user.id)
    reservas_paseador = Reserva.objects.filter(horario_paseo__paseador=paseador)
    cantidad_solicitudes = reservas_paseador.filter(estado = 'pendiente').count()

    data = {
        'cantidad_solicitudes':cantidad_solicitudes,
    }

    return render(request, "paseador/interfaz.html", data)


@verificar_usuario_paseador
def listar_horario(request):
    paseador_id = request.user.id
    paseador = Paseador.objects.get(pk=paseador_id)
    horarios = paseador.horariopaseo_set.all().order_by("dia", "hora_inicio")

    orden_dias = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]
    horarios_por_dia = {dia: [] for dia in orden_dias}

    for horario in horarios:
        horarios_por_dia[horario.dia].append(horario)

    horarios_ordenados = []
    for dia in orden_dias:
        horarios_ordenados.extend(horarios_por_dia[dia])

    data = {"horarios": horarios, "horarios_por_dia": horarios_por_dia}
    return render(request, "paseador/horarios/listar_horarios.html", data)


@verificar_usuario_paseador
def registrar_horario_paseo(request):
    paseador_id = request.user.id
    paseador = Paseador.objects.get(pk=paseador_id)

    if request.method == "POST":
        formulario = HorarioPaseoForm(request.POST)
        if formulario.is_valid():
            horario = formulario.save(commit=False)
            horario.paseador = paseador

            # Convertir hora_inicio a datetime para realizar la comparación
            hora_inicio_datetime = datetime.combine(datetime.now().date(), horario.hora_inicio)
            
            # Calcular el final del horario considerando la fecha actual
            hora_fin_datetime = hora_inicio_datetime + timedelta(hours=1)
            
            # Verificar si ya existe un horario registrado para el mismo día
            horarios_existentes = HorarioPaseo.objects.filter(
                paseador=paseador,
                dia=horario.dia,
                # Verificar superposición con horarios existentes
                hora_inicio__lt=hora_fin_datetime,
                hora_fin__gt=hora_inicio_datetime
            )

            if horarios_existentes.exists():
                messages.error(
                    request, "Ya tienes registrado un horario para este día y hora."
                )

                return redirect(to="paseador:registrar-horario")

            horario.save()
            messages.success(request, "Registrado correctamente.")
            return redirect(to="paseador:listar-horario")
    else:
        formulario = HorarioPaseoForm()

    data = {"formulario": formulario}

    return render(request, "paseador/horarios/registrar_horario.html", data)


@verificar_paseeador_horario
@verificar_usuario_paseador
def modificar_horario(request, id):
    horario = get_object_or_404(HorarioPaseo, id=id)
    data = {
        "form": HorarioPaseoForm(instance=horario),
        "horario": horario,
    }

    if request.method == "POST":
        formulario = HorarioPaseoForm(data=request.POST, instance=horario)
        paseador = Paseador.objects.get(pk=request.user.id)
        if formulario.is_valid():
            horario_modificado = formulario.save(commit=False)
            horario_modificado.paseador = paseador

            # Convertir hora_inicio a datetime para realizar la comparación
            hora_inicio_datetime = datetime.combine(datetime.now().date(), horario.hora_inicio)
            
            # Calcular el final del horario considerando la fecha actual
            hora_fin_datetime = hora_inicio_datetime + timedelta(hours=1)
            
            # Verificar si ya existe un horario registrado para el mismo día
            horarios_existentes = HorarioPaseo.objects.filter(
                paseador=paseador,
                dia=horario.dia,
                # Verificar superposición con horarios existentes
                hora_inicio__lt=hora_fin_datetime,
                hora_fin__gt=hora_inicio_datetime
            )

            if horarios_existentes.exists():
                messages.error(
                    request, "Ya tienes registrado un horario para este día y hora."
                )
                return redirect(to="paseador:listar-horario")

            horario_modificado.save()
            messages.info(request, "Modificado correctamente.")
            return redirect(to="paseador:listar-horario")
        data["form"] = formulario
    return render(request, "paseador/horarios/modificar_horario.html", data)


@verificar_paseeador_horario
@verificar_usuario_paseador
def eliminar_horario(request, id):
    horario = get_object_or_404(HorarioPaseo, id=id)
    horario.delete()
    messages.success(request, "Horario eliminado.")
    return redirect(to="paseador:listar-horario")


# editar perfil cliente

def update_profile(request):
    user = request.user
    paseador = user.paseador
    
    if request.method == 'POST':
        form = PaseadorUpdateForm(request.POST, request.FILES, instance=paseador)
        if form.is_valid():
            paseador = form.save(commit=False)
            print(user.password)
            user.save(update_fields=['telefono', 'direccion', 'comuna','edad'])
            print(user.password)
            paseador.save()
            return redirect('paseador:perfil-paseador')
        else:
            print(form.errors)
    else:
        initial_data = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'edad': paseador.edad,
            'direccion': paseador.direccion,
            'telefono': paseador.telefono,
            'comuna': paseador.comuna
        }
        form = PaseadorUpdateForm(initial=initial_data, instance=paseador)
    return render(request, 'paseador/perfil/perfil.html', {'form': form})