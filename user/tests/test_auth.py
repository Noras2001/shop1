import pytest
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_authentication(user):
    """
    Проверяет, может ли пользователь пройти аутентификацию с действительными учетными данными.
    """
    authenticated_user = authenticate(username="testuser", password="password")
    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"

@pytest.mark.django_db
def test_user_authentication_invalid_password(user):
    """
    Проверяет, что пользователь не может пройти аутентификацию с неправильным паролем.
    """
    authenticated_user = authenticate(username="testuser", password="wrongpassword")
    assert authenticated_user is None
