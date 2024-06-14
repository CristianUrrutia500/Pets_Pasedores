# cliente/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteCreationForm, Cliente, MascotaForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from .decorators import verificar_usuario_cliente, verificar_cliente_mascota
from django.contrib import messages
from usuario.models import User
from .models import Mascota
from paseador.models import Paseador
from collections import defaultdict
# email
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# verificación
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .forms import ClienteCreationForm, ClienteUpdateForm
from .models import Cliente


def registro_cliente(request):
    opciones = Cliente.COMUNAS_CHOICES
    data = {"form": ClienteCreationForm(), "opciones": opciones}
    if request.method == "POST":
        formulario = ClienteCreationForm(data=request.POST)
        if formulario.is_valid():
            # Guardar el formulario y obtener el usuario registrado
            usuario_registrado = formulario.save()
            # Obtener el grupo 'cliente'
            grupo = Group.objects.get(name="cliente")
            # Agregar el usuario al grupo
            grupo.user_set.add(usuario_registrado)
            # Desactiva la cuenta hasta la verificación del correo electrónico
            usuario_registrado.is_active = False  
            usuario_registrado.save()

            # Genera un token de verificación
            token = default_token_generator.make_token(usuario_registrado)

            # Enviar correo electrónico de verificación
            current_site = get_current_site(request)
            subject = 'Verifica tu cuenta'
            
            # Renderiza la plantilla HTML como texto plano
            text_content = render_to_string('registration/verification_email.txt', {
                'user': usuario_registrado,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario_registrado.pk)),
                'token': token,
            })
            
            # Envía el correo electrónico
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = usuario_registrado.email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.send()

            messages.success(request, "Por favor verifica tu correo electrónico para completar el registro.")
            return redirect('index')
        else:
            data["form"] = formulario

    return render(request, "registration/registro_cliente.html", data)


# Verificación de correo

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Si el token es válido, activa la cuenta del usuario
        user.is_active = True
        user.save()
        
        messages.success(request, "¡Tu correo electrónico ha sido verificado exitosamente!")
        return redirect('index')  # Redirecciona al índice de la página
    else:
        # Si el token no es válido, redirige a una página de error o muestra un mensaje
        messages.error(request, "El enlace de verificación no es válido.")
        return redirect('index')  # Redirecciona al índice de la página



# Entradas

@verificar_usuario_cliente
def interfaz_cliente(request):
    return render(request, "cliente/interfaz.html")


@verificar_usuario_cliente
def perfil_cliente(request):
    cliente = Cliente.objects.get(pk=request.user.id)
    return render(request, "cliente/perfil/perfil.html", {"cliente": cliente})
    pass


@verificar_usuario_cliente
def listar_mascotas(request):
    user_id = request.user.id
    cliente = Cliente.objects.get(pk=user_id)
    mascotas = cliente.mascota_set.all()
    data = {
        "mascotas": mascotas,
    }
    return render(request, "cliente/mascotas/listar_mascotas.html", data)


@verificar_usuario_cliente
def registrar_mascota(request):
    # Obtener el cliente específico
    cliente_id = request.user.id
    cliente = Cliente.objects.get(pk=cliente_id)
    opciones = Mascota.TAMANNO_CHOICES
    if request.method == "POST":
        # Si el formulario es enviado
        form = MascotaForm(request.POST, files=request.FILES)
        if form.is_valid():
            # Guardar la mascota asociada al cliente
            mascota = form.save(commit=False)
            mascota.duenno = cliente
            mascota.save()
            messages.success(request, "Registrado correctamente.")
            return redirect(to="cliente:lista-mascotas")
    else:
        # Si es un GET, mostrar el formulario vacío
        form = MascotaForm()

    data = {
        "form": form,
        "opciones":opciones,
    }

    return render(request, "cliente/mascotas/registrar_mascotas.html", data)


@verificar_usuario_cliente
@verificar_cliente_mascota
def modificar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    opciones = Mascota.TAMANNO_CHOICES
    data = {
        "form": MascotaForm(instance=mascota),
        "mascota": mascota,
        "opciones":opciones,
    }
    if request.method == "POST":
        formulario = MascotaForm(
            data=request.POST, instance=mascota, files=request.FILES
        )
        if formulario.is_valid():
            formulario.save()
            messages.info(request, "Modificado correctamente.")
            return redirect(to="cliente:lista-mascotas")
        data["form"] = formulario
    return render(request, "cliente/mascotas/modificar_mascota.html", data)


@verificar_usuario_cliente
@verificar_cliente_mascota
def eliminar_mascota(request, id):

    mascota = get_object_or_404(Mascota, id=id)
    mascota.delete()
    messages.success(request, "Mascota eliminada.")
    return redirect(to="cliente:lista-mascotas")


@verificar_usuario_cliente
def listar_paseadores(request):
    paseadores = Paseador.objects.all()
    comuna_query = request.GET.get("comuna")

    for paseador in paseadores:
        dias_disponibles = paseador.horariopaseo_set.values_list(
            "dia", flat=True
        ).distinct()
        dias_ordenados = sorted(
            dias_disponibles,
            key=lambda dia: [
                "lunes",
                "martes",
                "miercoles",
                "jueves",
                "viernes",
                "sabado",
                "domingo",
            ].index(dia),
        )
        paseador.dias_disponibles = dias_ordenados

    if comuna_query:
        paseadores = paseadores.filter(comuna__icontains=comuna_query)
    data = {"paseadores": paseadores}
    return render(request, "paseador/listar_paseadores.html", data)


def info_paseador(request, paseador_id):
    paseador = get_object_or_404(Paseador, pk=paseador_id)
    horarios = paseador.horariopaseo_set.all()

    # Crear un diccionario para almacenar los horarios ordenados
    horarios_por_dia_ordenados = {}

    # Agrupar los horarios por día de la semana
    for horario in horarios:
        dia = horario.dia
        if dia not in horarios_por_dia_ordenados:
            horarios_por_dia_ordenados[dia] = []
        horarios_por_dia_ordenados[dia].append((horario.id, str(horario.hora_inicio), str(horario.hora_fin)))

    dias_ordenados = {'lunes': 1, 'martes': 2, 'miercoles': 3, 'jueves': 4, 'viernes': 5, 'sabado': 6, 'domingo': 7}

    # Ordenar las listas de horarios por hora de inicio
    for dia, horarios in horarios_por_dia_ordenados.items():
        horarios_por_dia_ordenados[dia] = sorted(horarios, key=lambda x: (dias_ordenados[dia], x[1]))

    horarios_para_template = [{'dia': dia, 'horarios': horarios} for dia, horarios in sorted(horarios_por_dia_ordenados.items(), key=lambda x: dias_ordenados[x[0]])]

    data = {
        "horarios": horarios,
        "paseador": paseador,
        'horarios_para_template': horarios_para_template
    }
    return render(request, "paseador/info_paseador.html", data)

# editar perfil cliente

def update_profile(request):
    user = request.user
    cliente = user.cliente

    if request.method == 'POST':
        form = ClienteUpdateForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            print(user.password)
            user.save(update_fields=['telefono', 'direccion', 'comuna','edad'])
            print(user.password)
            cliente.save()
            return redirect('cliente:perfil-cliente')
        else:
            print(form.errors)
    else:
        initial_data = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'edad': cliente.edad,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'comuna': cliente.comuna
        }
        form = ClienteUpdateForm(initial=initial_data, instance=cliente)

    return render(request, 'cliente/perfil/perfil.html', {'form': form})