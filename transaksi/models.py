from django.db import models
from stok.models import Produk, JenisProvider, Pulsa
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.core.exceptions import ValidationError
from stok.models import Pulsa

class Transaksi(models.Model):
    jenisprovider = models.ForeignKey(JenisProvider, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    tanggal = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new transaction
            self.produk.jumlah_stok -= self.jumlah
            self.produk.save()  # Save changes to the product stock
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaksi {self.produk} - {self.jumlah} unit"

    def hitung_margin(self):
        return (self.produk.harga_jual - self.produk.harga_modal) * self.jumlah
    
class TransaksiPulsa(models.Model):
    pulsa = models.ForeignKey(Pulsa, on_delete=models.CASCADE, related_name='transaksi_pulsas')
    jumlah = models.DecimalField(max_digits=15, decimal_places=0)
    nomor_hp = models.CharField(max_length=15)
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Transaksi Pulsa - {self.jumlah} unit"

    def hitung_margin(self):
        """
        Calculate the fixed margin of 2000 for each pulsa transaction.
        """
        return 2000

    
