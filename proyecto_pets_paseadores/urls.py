"""
URL configuration for proyecto_pets_paseadores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views 

from django.conf import settings
from django.conf.urls.static import static
from .views import index, buy, pet, service, cerrar_sesion, CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("buy/", buy, name="buy"),
    # path('contact/', contact, name="contact"),
    path("pet/", pet, name="pet"),
    path("service/", service, name="service"),
    path("salir", cerrar_sesion, name="cerrar_sesion"),                 # cerrar sesion
    path('accounts/login/', CustomLoginView.as_view(), name='login'),   # accounts / login
    path("", include("administrador.urls",)),                           # administrador
    path("cliente/", include(("cliente.urls","cliente"))),              # cliente
    path("paseador/", include(("paseador.urls","paseador"))),           # paseador
    path('reset/', include('reset.urls')),                              # reset
    path('', include('reserva.urls')),                                  # reserva
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, root_document=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
