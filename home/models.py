from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import format_html
from taggit.managers import TaggableManager
from django.db.models import Avg
from django.db.models.signals import post_save


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
    color = models.ManyToManyField('Color', blank=True)
    size = models.ManyToManyField('Size', blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True)
    image = models.FileField(upload_to='product/%Y/%m/&d')
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.PositiveIntegerField(default=0)
    favourite = models.ManyToManyField(User, blank=True, related_name='fa_user')
    total_favourite = models.IntegerField(default=0)
    sell = models.IntegerField(default=0)
    view = models.ManyToManyField(User, blank=True, related_name='product_view')
    num_view = models.IntegerField(default=0)

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

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.id])

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
    update = models.DateTimeField(auto_now=True)

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


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chart(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    unit_price = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='pr_update')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True, related_name='v_update')

    def __str__(self):
        return self.name


def product_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(product=data, unit_price=data.unit_price, update=data.update, name=data.name)


post_save.connect(product_post_saved, sender=Product)


def variant_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(variant=data, unit_price=data.unit_price,
                         update=data.update, name=data.name,
                         size=data.size_variant, color=data.color_variant)


post_save.connect(variant_post_saved, sender=Variant)
