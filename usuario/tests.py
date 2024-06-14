from django.test import TestCase
from django.urls import reverse
from .models import User


""" class UsuarioTestCase(TestCase):
    def test_registro_usuario_url_resolves(self):
        url = reverse('registro-usuario')
        self.assertEqual(url, '/ruta/esperada/para/el/registro/de/usuario/')
        # Agrega más pruebas para las URLs de usuario aquí

    def test_registro_usuario(self):
        # Prueba para asegurar que el registro de usuario funciona correctamente
        # Puedes crear un usuario de prueba aquí y verificar que se haya creado correctamente
        # Ejemplo:
        response = self.client.post(reverse('registro-usuario'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'edad': 25,
            'direccion': 'Dirección de prueba',
            'telefono': '123456789',
            'comuna': 'La Florida'
        })
        # Asegúrate de verificar que la respuesta sea un redireccionamiento exitoso o cualquier otro comportamiento esperado

    # Agrega más pruebas para las vistas de usuario aquí
 """