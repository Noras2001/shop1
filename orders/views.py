from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        # Carrito vacío, redirige o muestra mensaje
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        address = request.POST.get('address')
        delivery_date = request.POST.get('delivery_date')
        delivery_time = request.POST.get('delivery_time')
        comment = request.POST.get('comment')

        # Crear Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            comment=comment
        )

        total = 0
        # Pasar items del carrito al pedido
        for item in cart.items.select_related('product'):
            price = item.product.price
            quantity = item.quantity
            total += price * quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=quantity,
                price=price,
            )

        order.total = total
        order.save()

        # Vaciar carrito o eliminarlo
        cart.delete()

        # Aquí podrías redirigir a una página de confirmación
        return redirect('checkout:order_success', order_id=order.id)

    return render(request, 'checkout/order_form.html')
