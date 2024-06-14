# proyecto_pets_paseadores/test_Pr.py

import pytest
from django.test import Client

@pytest.fixture
def cliente():
    return Client()

def test_index(cliente):
    # Verificar que la página de inicio devuelve un código de estado 200
    response = cliente.get('/')
    assert response.status_code == 200
