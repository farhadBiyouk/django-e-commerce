from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'product', 'variant', 'size', 'order', 'quantity']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'create', 'paid']
    inlines = [OrderItemAdmin]


admin.site.register(OrderItem)
