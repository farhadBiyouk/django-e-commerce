from django.urls import path
from home.views import (
    home,
    all_product,
    product_detail,
    product_like,
    product_unlike,
)

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('products/', all_product, name='all_product'),
    path('detail/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<slug>/', all_product, name='category'),
    path('like/<int:id>/', product_like, name='product_like'),
    path('unlike/<int:id>/', product_unlike, name='product_unlike'),
]
