import django_filters
from django import forms
from home.models import Product, Variant, Brand, Size, Color


class ProductFilter(django_filters.FilterSet):
    CHOICES_1 = (
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    )

    CHOICES_2 = (
        ('جدید ترین', 'جدید ترین'),
        ('قدیمی تر', 'قدیمی تر'),
    )

    CHOICES_3 = (
        ('پر تخفیف', 'پر تخفیف'),
        ('کم تخفیف', 'کم تخفیف'),
    )
    price1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=CHOICES_1, method='price_filter')
    create = django_filters.ChoiceFilter(choices=CHOICES_2, method='time_filter')
    discount = django_filters.ChoiceFilter(choices=CHOICES_3, method='discount_filter')

    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    def time_filter(self, queryset, name, value):
        data = 'create' if value == 'قدیمی تر' else '-create'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value == 'پر تخفیف' else '-discount'
        return queryset.order_by(data)
