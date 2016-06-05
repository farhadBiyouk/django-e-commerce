from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import format_html
from taggit.managers import TaggableManager
from django.db.models import Avg


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub')
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, allow_unicode=True, unique=True, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='category/%Y/%m/&d', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug])


class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comment_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', null=True, blank=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class Product(models.Model):
    VARIANT = (
        ('None', 'none'),
        ('Size', 'size'),
        ('Color', 'color'),
    )

    category = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    information = models.TextField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, choices=VARIANT)
    image = models.FileField(upload_to='product/%Y/%m/&d')
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="150px" height="75">')

    def average(self):
        data = Comment.objects.filter(is_reply=False, product=self).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'], 1)
        return star


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=200)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class ImageProductGallery(models.Model):
    name = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='porduct_image')
    image = models.FileField(upload_to='product_image_gallery/%Y/%m/&d', blank=True)

    def __str__(self):
        return self.name
