from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.auth.views import LoginView
from django.contrib import messages
# Request: Para realizar perticiones.
# HttpResponse: Para enviar la respuesta usando el protocolo HTTP.

def index(request):
    return render(request, "navegacion/index.html")
    
def buy(request):
    return render(request, "navegacion/buy.html")

# def contact(request):
#     return render(request, "navegacion/contact.html")

def pet(request):
    return render(request, "navegacion/pet.html")

def service(request):
    return render(request, "navegacion/service.html")

def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Sesion finalizada")
    return redirect(to="index")

# notificaciónes login

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Inicio de sesión fallido.\nPor favor, verifica tu usuario y contraseña e intenta nuevamente.")
        return super().form_invalid(form)