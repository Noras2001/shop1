import pytest
from django.urls import reverse
from catalog.models import Product, Category


@pytest.fixture
def category(db):
    """
    Crea una categoría para usar en pruebas.
    """
    return Category.objects.create(name="Flores", slug="flores")

@pytest.fixture
def product(db, category):
    """
    Crea un producto asociado a una categoría.
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
    Verifica que la vista del catálogo responde correctamente
    y contiene información del producto.
    """
    url = reverse('catalog:product_list')  # Ajusta según tu configuración de URLs
    response = client.get(url)

    assert response.status_code == 200
    assert product.name in response.content.decode()


