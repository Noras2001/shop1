from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order, OrderItem
from cart.models import Cart
from .forms import OrderForm

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

    if request.method == 'POST':
        # El usuario confirma definitivamente la orden
        # Vaciar el carrito, si no lo hiciste antes
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.delete()

        return redirect('orders:order_success', order_id=order.id)

    # GET: muestra resumen para confirmación
    # Podrías mostrar en la plantilla:
    # - Dirección, fecha/hora
    # - Ítems
    # - Total
    return render(request, 'orders/order_confirm.html', {'order': order})


@login_required
def order_success(request, order_id):
    # Mostrar la pantalla de confirmación
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

