from django import forms
from .models import Transaksi, TransaksiPulsa
from stok.models import Produk, Pulsa
from django import forms
from .models import TransaksiPulsa
from django.core.exceptions import ValidationError


class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['jenisprovider', 'produk', 'jumlah']
        labels = {
            'jenisprovider': 'Jenis Provider',
            'produk': 'Produk',
            'jumlah': 'Jumlah',
        }
        widgets = {
            'jenisprovider': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'produk': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Masukkan Jumlah'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jenisprovider'].empty_label = "Silahkan pilih"
        self.fields['produk'].empty_label = "Silahkan pilih"

class TransaksiPulsaForm(forms.ModelForm):
    nomor_hp = forms.CharField(max_length=15)

    class Meta:
        model = TransaksiPulsa
        fields = ['jumlah', 'nomor_hp']

    def clean_nomor_hp(self):
        nomor_hp = self.cleaned_data.get('nomor_hp')
        # Hapus spasi tambahan dan pastikan nomor dimulai dengan +62
        nomor_hp = nomor_hp.strip().replace(" ", "")
        
        # Pastikan nomor dimulai dengan +62, dan jika tidak, tambahkan
        if not nomor_hp.startswith('+62'):
            nomor_hp = '+62' + nomor_hp
        
        # Validasi bahwa setelah +62, hanya digit yang mengikuti
        if not nomor_hp[3:].isdigit():
            raise ValidationError("Nomor HP harus berupa angka setelah kode negara (+62).")
        
        return nomor_hp

    def clean(self):
        cleaned_data = super().clean()
        jumlah = cleaned_data.get("jumlah")

        # Pastikan jumlah (amount) lebih besar dari nol
        if jumlah is None or jumlah <= 0:
            raise forms.ValidationError("Jumlah harus lebih besar dari nol.")
        
        return cleaned_data
    

