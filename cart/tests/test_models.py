import pytest
from cart.models import Cart, CartItem

@pytest.mark.django_db
def test_cart_creation(cart):
    """
    Verifica que un carrito se crea correctamente.
    """
    assert Cart.objects.count() == 1
    assert cart.user.username == "testuser"
    assert cart.items.count() == 0  # Sin elementos al inicio

@pytest.mark.django_db
def test_cart_item_creation(cart_item):
    """
    Verifica que un elemento del carrito se crea correctamente.
    """
    assert CartItem.objects.count() == 1
    assert cart_item.quantity == 2
    assert cart_item.product.name == "Laptop"

@pytest.mark.django_db
def test_cart_item_relationship(cart_item):
    """
    Verifica la relación entre carrito y elementos del carrito.
    """
    assert cart_item.cart.items.count() == 1
    assert cart_item.cart == cart_item.cart
