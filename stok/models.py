from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

# Existing models

class Jenis(models.Model):
    nama_jenis = models.CharField(max_length=100, unique=True)
    tanggal_input = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_jenis

class Provider(models.Model):
    nama_provider = models.CharField(max_length=100, unique=True)
    tanggal_input = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_provider

class JenisProvider(models.Model):
    jenis = models.ForeignKey(Jenis, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    tanggal_input = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jenis} - {self.provider}"

class Produk(models.Model):
    nama_produk = models.CharField(max_length=100)
    jenis_provider = models.ForeignKey(JenisProvider, on_delete=models.CASCADE)
    harga_modal = models.DecimalField(max_digits=15, decimal_places=0)  # Hapus decimal_places dan default
    harga_jual = models.DecimalField(max_digits=15, decimal_places=0)  # Hapus decimal_places dan default
    jumlah_stok = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nama_produk

    def clean(self):
        if self.harga_modal < 0:
            raise ValidationError("Harga modal tidak boleh kurang dari nol.")
        if self.harga_jual < self.harga_modal:
            raise ValidationError("Harga jual tidak boleh kurang dari harga modal.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate model fields
        super().save(*args, **kwargs)  # Save the instance to the database

    def hitung_harga_jual(self, markup=None):
        """
        Method to calculate selling price based on purchase price (harga_modal) and markup.
        """
        if self.jenis_provider.jenis.nama_jenis.lower() == 'pulsa':
            if markup is None:
                markup = 2000  # Default markup for pulsa
            self.harga_jual = self.harga_modal + markup
        else:
            self.harga_jual = self.harga_modal  # For other products, use harga_modal as harga_jual
        return self.harga_jual

# New model for Pulsa

class Pulsa(models.Model):
    saldo = models.DecimalField(
        max_digits=15, 
        decimal_places=0, 
        help_text="Input nominal saldo"
    )
    tanggal_input = models.DateField(auto_now_add=True, editable=False)  # Closed parenthesis

    def __str__(self):
        return f"Saldo: {self.saldo}"

    def clean(self):
        if self.saldo < 0:
            raise ValidationError("Saldo tidak boleh kurang dari nol.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate model fields
        super().save(*args, **kwargs)  # Save the instance to the database

    def hitung_harga_jual(self):
        """
        Method to calculate selling price based on balance (saldo) and fixed markup.
        """
        markup = 2000  # Fixed markup for every transaction
        harga_jual = self.saldo + markup
        return harga_jual
    
class PulsaTotal(models.Model):
    total_saldo = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        help_text="Total saldo of all Pulsa entries"
    )
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def update_total_saldo(cls):
        from django.db.models import Sum
        total = Pulsa.objects.aggregate(total_saldo=Sum('saldo'))['total_saldo'] or 0
        obj, created = cls.objects.get_or_create(pk=1)  # Ensure a record is created if not found
        obj.total_saldo = total
        obj.save()
    


