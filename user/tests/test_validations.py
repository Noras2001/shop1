import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_phone_validation():
    """
    Verifica que el campo phone no acepte valores inválidos.
    """
    user = User(username="invalidphone", phone="invalid")
    with pytest.raises(ValidationError):
        user.full_clean()  # Valida el modelo
