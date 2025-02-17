# authapp/urls.py
from django.urls import path
from . import views
from authapp import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import custom_logout


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),  # Pastikan ini ada
    path('cashier-dashboard/', views.cashier_dashboard, name='cashier_dashboard'), # Tambahkan ini
    path('logout/', LogoutView.as_view(), name='logout'),
    

]
