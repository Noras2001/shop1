from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
        else:
            # Si la cantidad es 0 o negativa, puedes eliminar el item
            cart_item.delete()

    return redirect('cart:cart_detail')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Obtener el carrito actual (si no existe, crearlo)
    # Aquí asumimos que el usuario está logueado:
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Buscar si el ítem ya está en el carrito
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = None
    items = []
    total = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            items = cart.items.select_related('product')
            total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total
    })

