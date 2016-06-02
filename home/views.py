from django.shortcuts import render, get_object_or_404, redirect
from home.models import Category, Product, Variant
from django.contrib import messages


def home(request):
    categories = Category.objects.filter(is_sub=False)
    return render(request, 'home/home.html', {'categories': categories})


def all_product(request, slug=None):
    products = Product.objects.all()
    category = Category.objects.filter(is_sub=False)
    if slug:
        data = Category.objects.get(slug=slug)
        products = products.filter(category=data)
    return render(request, 'home/product.html', {'products': products, 'category': category})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    if product.status is not None:
        if request.method == 'POST':
            variant = Variant.objects.filter(product_variant_id=product_id)
            variants = Variant.objects.get(id=request.POST.get('select'))
        else:
            variant = Variant.objects.filter(product_variant_id=product_id)
            variants = Variant.objects.get(id=variant[0].id)
        return render(request, 'home/detail.html',
                      {'product': product, 'variant': variant, 'variants': variants, 'is_like': is_like})
    else:
        return render(request, 'home/detail.html', {'product': product, 'is_like': is_like})


def product_like(request, id):
    product = get_object_or_404(Product, pk=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
        messages.warning(request, 'remove like')
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request, 'added  your like tnx')

    return redirect(request.META.get('HTTP_REFERER'))


def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, pk=id)
    product.unlike.add(request.user)
    print(url)
    return redirect(url)
