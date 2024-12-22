import pytest
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_authentication(user):
    """
    Verifica que un usuario puede autenticarse con credenciales válidas.
    """
    authenticated_user = authenticate(username="testuser", password="password")
    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"

@pytest.mark.django_db
def test_user_authentication_invalid_password(user):
    """
    Verifica que un usuario no puede autenticarse con una contraseña incorrecta.
    """
    authenticated_user = authenticate(username="testuser", password="wrongpassword")
    assert authenticated_user is None
