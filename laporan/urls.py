from django.urls import path
from .views import (
    produk_report, pulsa_report, export_produk_to_excel, export_pulsa_to_excel,
    laporan_home, transaksi_report, transaksi_pulsa_report,
    export_transaksi_to_excel, export_transaksi_pulsa_to_excel
)

urlpatterns = [
    path('', laporan_home, name='laporan_home'),
    path('produk/', produk_report, name='produk_report'),
    path('pulsa/', pulsa_report, name='pulsa_report'),
    path('export_produk/', export_produk_to_excel, name='export_produk_to_excel'),
    path('export_pulsa/', export_pulsa_to_excel, name='export_pulsa_to_excel'),
    path('transaksi/', transaksi_report, name='transaksi_report'),
    path('transaksi_pulsa/', transaksi_pulsa_report, name='transaksi_pulsa_report'),
    path('export_transaksi/', export_transaksi_to_excel, name='export_transaksi_to_excel'),
    path('export_transaksi_pulsa/', export_transaksi_pulsa_to_excel, name='export_transaksi_pulsa_to_excel'),
]
