from django.contrib import admin
from order.models import Order, OrderItem, Coupon


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'product', 'variant', 'size', 'order', 'quantity', 'price']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'create', 'paid', 'get_price']
    inlines = [OrderItemAdmin]


admin.site.register(OrderItem)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start', 'end', 'discount', 'active']
