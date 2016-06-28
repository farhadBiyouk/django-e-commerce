from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from order.forms import OrderForm, CouponForm
from order.models import Order, OrderItem, Coupon
from cart.models import Cart
from django.views.decorators.http import require_POST


def detail_order(request, id):
    order = Order.objects.get(id=id)
    form = CouponForm()
    return render(request, 'order/detail.html', {'order': order, 'form': form})


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


@require_POST
def coupon_order(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        data = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=data, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExisr:
            messages.warning(request, 'this code wrong')
            return redirect('order:detail_order', order_id)

        order.discount = coupon.discount
        order.save()
        return redirect('order:detail_order', order_id)
