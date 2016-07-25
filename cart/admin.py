from django.contrib import admin
from cart.models import Cart, Compare


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'variant', 'quantity']


admin.site.register(Compare)