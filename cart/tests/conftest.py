import pytest
from cart.models import Cart, CartItem
from catalog.models import Product, Category
from django.contrib.auth import get_user_model

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics", slug="electronics")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Laptop",
        slug="laptop",
        category=category,
        price=1500.00,
        stock=20
    )

@pytest.fixture
def cart(db, user):
    return Cart.objects.create(user=user)

@pytest.fixture
def cart_item(db, cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=2)
