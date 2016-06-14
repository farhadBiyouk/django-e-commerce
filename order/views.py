from django.shortcuts import render, redirect
from order.forms import OrderForm
from order.models import Order, OrderItem
from cart.models import Cart


def detail_order(request, id):
    order = Order.objects.get(id=id)
    return render(request, 'order/detail.html', {'order': order})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(
                user_id=request.user.id,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                address=data['address']
            )
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                OrderItem.objects.create(
                    order_id=order.id,
                    product_id=c.product_id,
                    variant_id=c.variant_id,
                    quantity=c.quantity,
                    user_id=request.user.id
                )
            Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order:detail_order', order.id)
