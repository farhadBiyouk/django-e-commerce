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
    path('active/<uidb64>/<token>/', views.EmailRegister.as_view(), name='active'),
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/done/', views.ResetPasswordDone.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(), name='password_reset_complete'),

]
