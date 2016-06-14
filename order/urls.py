from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
    path('<int:id>', views.detail_order, name='detail_order'),
    path('create/', views.create_order, name='create_order'),
]
