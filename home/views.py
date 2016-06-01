from django.shortcuts import render, get_object_or_404
from home.models import Category, Product, Variant


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
    if product.status is not None:
        if request.method == 'POST':
            variant = Variant.objects.filter(product_variant_id=product_id)
            variants = Variant.objects.get(id=request.POST.get('select'))
        else:
            variant = Variant.objects.filter(product_variant_id=product_id)
            variants = Variant.objects.get(id=variant[0].id)
        return render(request, 'home/detail.html', {'product': product, 'variant': variant, 'variants': variants})
    else:
        return render(request, 'home/detail.html', {'product': product})
