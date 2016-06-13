from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.detail, name='detail_cart'),
    path('add/<int:id>/', views.add_cart, name='add_cart'),
    path('remove/<int:id>/', views.remove_cart, name='remove_cart'),
]
