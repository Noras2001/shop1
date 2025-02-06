import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_phone_validation():
    """
    Мы проверяем, что поле телефона не принимает недопустимых значений.
    """
    user = User(username="invalidphone", phone="invalid")
    with pytest.raises(ValidationError):
        user.full_clean()  # Проверяет модель
