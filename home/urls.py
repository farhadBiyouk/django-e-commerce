from django.urls import path
from home.views import (
    home,
    all_product,
    product_detail
)

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('products/', all_product, name='all_product'),
    path('detail/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<slug>/', all_product, name='category')
]
