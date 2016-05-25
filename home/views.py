from django.shortcuts import render, get_object_or_404
from home.models import Category, Product


def home(request):
    categories = Category.objects.all()
    return render(request, 'home/home.html', {'categories': categories})


def all_product(request, slug=None):
    products = Product.objects.all()
    category = Category.objects.all()
    if slug:
        data = Category.objects.get(slug=slug)
        products = products.filter(category=data)
    return render(request, 'home/product.html', {'products': products, 'category': category})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'home/detail.html', {'product': product})
