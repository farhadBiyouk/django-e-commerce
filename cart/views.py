from django.shortcuts import render, redirect
from cart.forms import CartForm
from .models import Cart
from home.models import Product, Variant
from django.contrib import messages
from order.forms import OrderForm


def detail(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    order_form = OrderForm()
    total = 0
    for p in cart:
        if p.product.status != 'None':
            total += p.variant.total_price * p.quantity
        else:
            total += p.product.total_price * p.quantity
    return render(request, 'cart/detail.html', {'cart': cart, 'total': total, 'order_form': order_form})


def add_cart(request, id):
    product = Product.objects.get(id=id)
    if product.status != 'None':
        data = Cart.objects.filter(user_id=request.user.id, variant_id=request.POST.get('select'))
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            quantity_number = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != 'None':
                    shop = Cart.objects.get(user_id=request.user.id, product_id=id,
                                            variant_id=request.POST.get('select'))
                else:
                    shop = Cart.objects.get(user_id=request.user.id, product_id=id)
                shop.quantity += quantity_number
                shop.save()
                messages.success(request, 'updated  product successfully')
            else:
                Cart.objects.create(
                    user_id=request.user.id,
                    product_id=id,
                    variant_id=request.POST.get('select'),
                    quantity=quantity_number
                )
                messages.success(request, 'added new product to cart')
        return redirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, id):
    Cart.objects.get(id=id).delete()
    messages.success(request, 'deleted  product from cart successfully')
    return redirect(request.META.get('HTTP_REFERER'))


def add_single(request, id):
    cart = Cart.objects.get(id=id)
    if cart.product.status == 'None':
        product = Product.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1

    else:
        variant = Variant.objects.get(id=cart.variant.id)
        if variant.amount > cart.quantity:
            cart.quantity += 1
    cart.save()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_single(request, id):
    cart = Cart.objects.get(id=id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
    cart.save()
    return redirect(request.META.get('HTTP_REFERER'))
