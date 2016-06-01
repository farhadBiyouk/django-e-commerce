from django.contrib import admin
from home.models import Category, Product, Size, Color, Variant


class VariantAdmin(admin.TabularInline):
    model = Variant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'create', 'update']
    list_filter = ('create',)
    prepopulated_fields = {'slug': ['name']}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit_price', 'amount', 'discount', 'total_price', 'available']
    list_filter = ('available',)
    inlines = (VariantAdmin,)


admin.site.register(Size)
admin.site.register(Color)
