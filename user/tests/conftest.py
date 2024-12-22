import pytest
from django.contrib.auth import get_user_model
# Фикстуры для тестов
@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password", phone="+71234567890")
