import pytest
from django.contrib.auth.models import User
from django.test import Client

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    """
    Verifica que un usuario se crea correctamente.
    """
    user = User.objects.create_user(username="testuser", password="password", phone="+71234567890")
    assert User.objects.count() == 1
    assert user.username == "testuser"
    assert user.phone == "+71234567890"

@pytest.mark.django_db
def test_user_str_method(user):
    """
    Verifica que el método __str__ devuelve el username.
    """
    assert str(user) == "testuser"

@pytest.mark.django_db
def test_user_phone_optional(db):
    """
    Verifica que el campo phone es opcional.
    """
    user = User.objects.create_user(username="nophone", password="password")
    assert user.phone is None


