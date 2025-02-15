from django.urls import path
from home.views import (
    home,
    all_product,
    product_detail,
    product_like,
    product_unlike,
    product_comment,
    product_rely_comment,
    search_product,
    favourite_product,
    contact,
)

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('products/', all_product, name='all_product'),
    path('detail/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<slug>/', all_product, name='category'),
    path('like/<int:id>/', product_like, name='product_like'),
    path('unlike/<int:id>/', product_unlike, name='product_unlike'),
    path('comment/<int:id>/', product_comment, name='product_comment'),
    path('reply/<int:id>/<int:comment_id>/', product_rely_comment, name='product_rely_comment'),
    path('search/', search_product, name='search_product'),
    path('favourite/<int:id>', favourite_product, name='favourite_product'),
    path('contact/', contact, name='contact'),
]
