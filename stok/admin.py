from django.contrib import admin
from .models import Jenis, Provider, JenisProvider, Produk, Pulsa

@admin.register(Jenis)
class JenisAdmin(admin.ModelAdmin):
    list_display = ('nama_jenis', 'tanggal_input')
    readonly_fields = ('tanggal_input',)

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('nama_provider', 'tanggal_input')
    readonly_fields = ('tanggal_input',)

@admin.register(JenisProvider)
class JenisProviderAdmin(admin.ModelAdmin):
    list_display = ('jenis', 'provider', 'tanggal_input')
    readonly_fields = ('tanggal_input',)

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('nama_produk', 'jenis_provider', 'harga_modal', 'harga_jual', 'jumlah_stok')
    readonly_fields = ('harga_jual',)

@admin.register(Pulsa)
class PulsaAdmin(admin.ModelAdmin):
    list_display = ('saldo', 'tanggal_input')
    readonly_fields = ('tanggal_input',)


