from django.contrib import admin
from django.urls import path, include
from authapp import views as auth_views
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib import admin
from stok import views
from stok.views import stok_list_admin, tambah_stok_admin
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from authapp import views as auth_views
from stok import views as stok_views
from transaksi import views as transaksi_views
from laporan import views as laporan_views
from django.contrib import admin
from django.urls import path, include
from authapp import views as auth_views
from django.shortcuts import redirect
from transaksi import views as transaksi_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),
    path('', include('authapp.urls')),
    path('home/', auth_views.home, name='home'),
    path('stok/', include('stok.urls')), 
    path('stok_admin/', stok_list_admin, name='stok_list_admin'),
    path('tambah_stok/', views.tambah_stok, name='tambah_stok'),
    path('jenis/', views.jenis_list, name='jenis_list'),
    path('providers/', views.provider_list, name='provider_list'),
    path('jenisprovider/', views.jenisprovider_list, name='jenisprovider_list'),
    path('provider/tambah/', views.tambah_provider, name='tambah_provider'),
    path('jenisprovider/', views.jenisprovider_list, name='jenisprovider_list'),
    path('jenisprovider/tambah/', views.tambah_jenisprovider, name='tambah_jenisprovider'),
    path('jenis/tambah_inline/', views.tambah_jenis_inline, name='tambah_jenis_inline'),
    path('edit_jenis/<int:jenis_id>/', views.edit_jenis, name='edit_jenis'),
    path('hapus_jenis/<int:jenis_id>/', views.hapus_jenis, name='hapus_jenis'),
    path('edit_provider/<int:provider_id>/', views.edit_provider, name='edit_provider'),
    path('hapus_provider/<int:provider_id>/', views.hapus_provider, name='hapus_provider'),
    path('jenisprovider/delete/<int:jenisprovider_id>/', views.delete_jenisprovider, name='delete_jenisprovider'),
    path('jenisprovider/edit/<int:jenisprovider_id>/', views.edit_jenisprovider, name='edit_jenisprovider'),
    path('produk/tambah/', views.produk_tambah, name='produk_tambah'),
    path('produk/<int:produk_id>/edit/', views.produk_edit, name='produk_edit'),
    path('produk/<int:produk_id>/hapus/', views.produk_hapus, name='produk_hapus'),
    path('pulsa/', views.pulsa_list, name='pulsa_list'),
    path('pulsa/<int:pulsa_id>/edit/', views.pulsa_edit, name='pulsa_edit'),
    path('pulsa/<int:pulsa_id>/hapus/', views.pulsa_hapus, name='pulsa_hapus'),
    path('transaksi/', include('transaksi.urls')),
    path('laporan/', include('laporan.urls')),

    # Admin
     path('tambah/', tambah_stok_admin, name='tambah_stok_admin'),
     path('pulsa_list/', views.pulsa_list_admin, name='pulsa_list_admin'),
     path('transaksi_admin/', transaksi_views.transaksi_list_admin, name='transaksi_list_admin'),
    path('transaksi_pulsa_admin/', transaksi_views.transaksi_pulsa_list_admin, name='transaksi_pulsa_list_admin'),
]
