from django.shortcuts import render, get_object_or_404, redirect
from home.models import Category, Product, Variant, Comment, ImageProductGallery
from django.contrib import messages
from home.forms import CommentProductForm, ReplyCommentProductForm, SearchForm
from django.db.models import Q
from cart.forms import CartForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from home.filters import ProductFilter
from urllib.parse import urlencode


def home(request):
    categories = Category.objects.filter(is_sub=False)
    return render(request, 'home/home.html', {'categories': categories})


def all_product(request, slug=None):
    products = Product.objects.all()
    filter_item = ProductFilter(request.GET, queryset=products)
    products = filter_item.qs
    pagination = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    category = Category.objects.filter(is_sub=False)
    if slug:
        data = Category.objects.get(slug=slug)
        page_obj = products.filter(category=data)
        pagination = Paginator(page_obj, 4)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)
    return render(request, 'home/product.html',
                  {'products': page_obj, 'category': category, 'filter_item': filter_item})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.num_view += 1
    product.save()
    if request.user.is_authenticated:
        product.view.add(request.user)
    comment_form = CommentProductForm()
    reply_comment = ReplyCommentProductForm()
    comments = Comment.objects.filter(product_id=product_id, is_reply=False)
    similar_product = product.tags.similar_objects()[:2]
    image_gallery = ImageProductGallery.objects.filter(product_id=product_id)
    cart_form = CartForm()
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    is_fav = False
    if product.favourite.filter(id=request.user.id).exists():
        is_fav = True
    if product.status != 'None':
        if request.method == 'POST':
            variant = Variant.objects.filter(product_variant_id=product_id)
            variants = Variant.objects.get(id=request.POST.get('select'))
        else:
            variant = Variant.objects.filter(product_variant_id=product_id)
            variants = Variant.objects.get(id=variant[0].id)
        return render(request, 'home/detail.html',
                      {'product': product, 'variant': variant, 'variants': variants, 'is_like': is_like,
                       'is_fav': is_fav,
                       'comments': comments, 'comment_form': comment_form, 'reply_comment': reply_comment,
                       'similar_product': similar_product, 'image_gallery': image_gallery, 'cart_form': cart_form})
    else:
        return render(request, 'home/detail.html',
                      {'product': product, 'is_like': is_like, 'is_fav': is_fav, 'comment_form': comment_form,
                       'comments': comments,
                       'reply_comment': reply_comment, 'similar_product': similar_product,
                       'image_gallery': image_gallery, 'cart_form': cart_form})


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


def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(
                user_id=request.user.id,
                product_id=id,
                comment=data['comment'],
                rate=data['rate']
            )
            messages.success(request, 'added new comment')
        return redirect(url)


def product_rely_comment(request, id, comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReplyCommentProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(
                comment=data['comment'],
                product_id=id,
                user_id=request.user.id,
                reply_id=comment_id,
                is_reply=True
            )
            messages.success(request, 'added successfully  reply comment, tank you')
        return redirect(url)


def search_product(request):
    product = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data is not None:
                if data.isdigit():
                    product = product.filter(
                        Q(discount__exact=data) |
                        Q(unit_price__exact=data)
                    )
                else:
                    product = product.filter(
                        Q(name__icontains=data)
                    )
    return render(request, 'home/product.html', {'products': product})


def favourite_product(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    is_fav = False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        is_fav = False
        product.total_favourite -= 1
        messages.error(request, 'deleted this product to your favourite list', 'danger')
    else:
        product.favourite.add(request.user)
        is_fav = True
        product.total_favourite += 1
        messages.success(request, 'added this product to your favourite list')
    return redirect(url)


def contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        body = subject + '\n' + email + '\n' + message
        form = EmailMessage(
            'Contact form',
            body,
            'test',
            ['beshkhom@gmail.com']
        )
        form.send(fail_silently=False)
        messages.success(request, 'sent email successfully')
    return render(request, 'home/contact.html')
