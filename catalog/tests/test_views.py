import pytest
from django.urls import reverse
from catalog.models import Product, Category


@pytest.fixture
def category(db):
    """
    Создайте категорию для использования при тестировании.
    """
    return Category.objects.create(name="Flores", slug="flores")

@pytest.fixture
def product(db, category):
    """
    Создание продукта, связанного с категорией.
    """
    return Product.objects.create(
        category=category,
        name="Розы",
        slug="roses",
        description="Flores frescas para cualquier ocasión.",
        price=100.00,
        stock=50,
        available=True
    )


@pytest.mark.django_db
def test_view_catalog(client, product):
    """
    Убедитесь, что представление каталога отвечает правильно
    и содержит информацию о продукте.
    """
    url = reverse('catalog:product_list')  # Настройте в соответствии с конфигурацией вашего URL
    response = client.get(url)

    assert response.status_code == 200
    assert product.name in response.content.decode()


