from django.contrib import admin
from home.models import (
    Category,
    Product,
    Size,
    Color,
    Variant,
    Comment,
    ImageProductGallery,
    Brand,
    Chart,
)
from django.utils.html import format_html


class VariantAdmin(admin.TabularInline):
    model = Variant
    extra = 1


class ImageGalleryAdmin(admin.TabularInline):
    model = ImageProductGallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'create', 'update']
    list_filter = ('create',)
    prepopulated_fields = {'slug': ['name']}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_category', 'show_image', 'unit_price', 'amount', 'discount', 'total_price',
                    'available']
    list_filter = ('available',)
    inlines = (VariantAdmin, ImageGalleryAdmin)

    def show_category(self, obj):
        return ', '.join([cat.name for cat in obj.category.all()])


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'rate']


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Chart)
