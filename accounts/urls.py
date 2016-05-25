from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('change/', views.change_password, name='change_password'),
]
