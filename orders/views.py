from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order, OrderItem
from cart.models import Cart
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Calcular total
            total = 0
            for item in cart.items.select_related('product'):
                total += item.product.price * item.quantity
            order.total = total
            order.save()

            # Crear OrderItems
            for item in cart.items.select_related('product'):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # No borramos el carrito aún si quieres permitir
            # al usuario volver atrás. Pero si deseas vaciarlo
            # aquí, hazlo.

            return redirect('orders:order_confirm', order_id=order.id)
        else:
            # Formulario no válido => errores
            return render(request, 'orders/order_form.html', {'form': form})
    else:
        # GET: formulario vacío
        form = OrderForm()
        return render(request, 'orders/order_form.html', {'form': form})


@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Si ya está confirmado, tal vez quieras redirigir a success directamente:
    if order.is_confirmed:
        return redirect('orders:order_success', order_id=order_id)

    if request.method == 'POST':
        # El usuario hizo clic en “Подтвердить заказ”
        order.is_confirmed = True
        order.save()
        return redirect('orders:order_success', order_id=order_id)

    # GET -> mostrar un resumen
    items = order.items.select_related('product')
    context = {
        'order': order,
        'items': items
    }
    return render(request, 'orders/order_confirm.html', context)

@login_required
def order_success(request, order_id):
    # Mostrar la pantalla de confirmación
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

