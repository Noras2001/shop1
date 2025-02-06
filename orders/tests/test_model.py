import pytest
from django.core.exceptions import ValidationError
from orders.models import Order, OrderItem
from catalog.models import Product, Category
from django.contrib.auth import get_user_model
from datetime import date, time

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def category(db):
    return Category.objects.create(name="Цветы", slug="flowers")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Розы",
        slug="roses",
        category=category,
        price=100.00,
        stock=10
    )

@pytest.fixture
def order(db, user):
    return Order.objects.create(
        user=user,
        address="ул. Примерная, д. 1",
        delivery_date=date(2024, 12, 25),
        delivery_time=time(15, 0),
        phone="+71234567890",
        email="test@example.com",
        payment_method="Карта",
        total=500.00,
        is_confirmed=True
    )

@pytest.fixture
def order_item(db, order, product):
    return OrderItem.objects.create(order=order, product=product, quantity=2, price=200.00)


# Тесты для модели Order
def test_order_creation(order):
    """Проверяет создание заказа и правильное сохранение данных."""
    assert Order.objects.count() == 1
    assert order.address == "ул. Примерная, д. 1"
    assert order.total == 500.00
    assert order.is_confirmed is True

def test_order_phone_validation(user):
    """Проверяет валидацию телефона при создании заказа."""
    with pytest.raises(ValidationError):
        order = Order(
            user=user,
            phone="12345"  # Неверный формат
        )
        order.full_clean()

# Тесты для модели OrderItem
def test_order_item_creation(order_item):
    """Проверяет создание элемента заказа и сохранение данных."""
    assert OrderItem.objects.count() == 1
    assert order_item.quantity == 2
    assert order_item.price == 200.00

def test_order_item_relationship(order_item, order, product):
    """Проверяет связи элемента заказа с заказом и продуктом."""
    assert order_item.order == order
    assert order_item.product == product
    assert order.items.count() == 1
