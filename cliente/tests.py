from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
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

class TestUrls(SimpleTestCase):
    def test_registro_cliente_url_resolves(self):
        url = reverse('registro-cliente')
        self.assertEquals(resolve(url).func, registro_cliente)

    """ def test_interfaz_cliente_url_resolves(self):
        url = reverse('interfaz-cliente')
        self.assertEquals(resolve(url).func, interfaz_cliente)

    def test_listar_mascotas_url_resolves(self):
        url = reverse('lista-mascotas')
        self.assertEquals(resolve(url).func, listar_mascotas)

    def test_registrar_mascota_url_resolves(self):
        url = reverse('registrar-mascotas')
        self.assertEquals(resolve(url).func, registrar_mascota)

    def test_modificar_mascota_url_resolves(self):
        url = reverse('modificar-mascota', args=['1'])
        self.assertEquals(resolve(url).func, modificar_mascota)

    def test_eliminar_mascota_url_resolves(self):
        url = reverse('eliminar-mascota', args=['1'])
        self.assertEquals(resolve(url).func, eliminar_mascota)

    def test_listar_paseadores_url_resolves(self):
        url = reverse('lista-paseadores')
        self.assertEquals(resolve(url).func, listar_paseadores)

    def test_perfil_cliente_url_resolves(self):
        url = reverse('perfil-cliente')
        self.assertEquals(resolve(url).func, perfil_cliente)

    def test_info_paseador_url_resolves(self):
        url = reverse('info-paseador', args=['1'])
        self.assertEquals(resolve(url).func, info_paseador)

    def test_verify_email_url_resolves(self):
        url = reverse('verify_email', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func, verify_email)

    def test_update_profile_url_resolves(self):
        url = reverse('update_profile')
        self.assertEquals(resolve(url).func, update_profile)
 """