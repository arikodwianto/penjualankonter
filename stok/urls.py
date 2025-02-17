from django.contrib import admin
from django.urls import path
from stok import views as stok_views
from . import views
from .views import stok_list_admin, tambah_stok_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.stok_list, name='stok_list'),
    path('stok_admin/', stok_list_admin, name='stok_list_admin'),
    path('produk/tambah/', stok_views.produk_tambah, name='produk_tambah'),
    path('produk/edit/<int:produk_id>/', stok_views.produk_edit, name='produk_edit'),
    path('produk/hapus/<int:produk_id>/', stok_views.produk_hapus, name='produk_hapus'),
    path('jenis/tambah/', stok_views.tambah_jenis_inline, name='tambah_jenis_inline'),
    path('jenis/edit/<int:jenis_id>/', stok_views.edit_jenis, name='edit_jenis'),
    path('jenis/hapus/<int:jenis_id>/', stok_views.hapus_jenis, name='hapus_jenis'),
    path('provider/tambah/', stok_views.tambah_provider, name='tambah_provider'),
    path('provider/edit/<int:provider_id>/', stok_views.edit_provider, name='edit_provider'),
    path('provider/hapus/<int:provider_id>/', stok_views.hapus_provider, name='hapus_provider'),
    path('jenisprovider/', stok_views.jenisprovider_list, name='jenisprovider_list'),
    path('jenisprovider/tambah/', stok_views.tambah_jenisprovider, name='tambah_jenisprovider'),
    path('jenisprovider/edit/<int:jenisprovider_id>/', stok_views.edit_jenisprovider, name='edit_jenisprovider'),
    path('jenisprovider/hapus/<int:jenisprovider_id>/', stok_views.delete_jenisprovider, name='hapus_jenisprovider'),
    path('stok/tambah/', stok_views.tambah_stok, name='tambah_stok'),
    path('pulsa/', views.pulsa_list, name='pulsa_list'),
   
    path('pulsa/<int:pulsa_id>/edit/', views.pulsa_edit, name='pulsa_edit'),
    path('pulsa/<int:pulsa_id>/hapus/', views.pulsa_hapus, name='pulsa_hapus'),
# urls.py

    path('tambah_saldo_pulsa/', views.tambah_saldo_pulsa, name='tambah_saldo_pulsa'),
    path('tambah_saldo_pulsa/<int:pulsa_id>/', views.tambah_saldo_pulsa, name='tambah_saldo_pulsa'),


    # Admin
    path('tambah/', tambah_stok_admin, name='tambah_stok_admin'),
    path('pulsa_list/', views.pulsa_list_admin, name='pulsa_list_admin'),
]
