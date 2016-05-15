from django.urls import path
from home.views import (
    home,
    all_product
)

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('products/', all_product, name='all_product'),
]
