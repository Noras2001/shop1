import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    """
    Проверка правильности создания пользователя.
    """
    user = User.objects.create_user(username="testuser", password="password", phone="+71234567890")
    assert User.objects.count() == 1
    assert user.username == "testuser"
    assert user.phone == "+71234567890"

@pytest.mark.django_db
def test_user_str_method(user):
    """
    Мы проверяем, что метод __str__ возвращает имя пользователя.
    """
    assert str(user) == "testuser"

@pytest.mark.django_db
def test_user_phone_optional(db):
    """
    Мы проверяем, что поле телефона является опциональным.
    """
    user = User.objects.create_user(username="nophone", password="password")
    assert user.phone is None


