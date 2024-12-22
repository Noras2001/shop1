import pytest
from cart.models import CartItem

@pytest.mark.django_db
def test_add_item_to_cart(cart, product):
    """
    Agregar un producto al carrito.
    """
    CartItem.objects.create(cart=cart, product=product, quantity=1)
    assert cart.items.count() == 1

@pytest.mark.django_db
def test_remove_item_from_cart(cart, product):
    """
    Eliminar un producto del carrito.
    """
    item = CartItem.objects.create(cart=cart, product=product, quantity=1)
    item.delete()
    assert cart.items.count() == 0

@pytest.mark.django_db
def test_update_item_quantity(cart_item):
    """
    Actualizar la cantidad de un producto en el carrito.
    """
    cart_item.quantity = 5
    cart_item.save()
    assert cart_item.quantity == 5
