from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaksi_list, name='transaksi_list'),    
    path('pulsa/', views.transaksi_pulsa_list, name='transaksi_pulsa_list'),
   path('transaksi_admin/', views.transaksi_list_admin, name='transaksi_list_admin'),
   path('transaksi_pulsa_admin/', views.transaksi_pulsa_list_admin, name='transaksi_pulsa_list_admin'),
]
