from django import forms
from decimal import Decimal  
from .models import Produk, Jenis, Provider, JenisProvider, Pulsa

class ThousandsSeparatorNumberInput(forms.NumberInput):
    def format_value(self, value):
        if value is None:
            return ''
        return f'{value:,}'.replace(',', '.')

class ThousandsSeparatorDecimalField(forms.DecimalField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        value = str(value).replace('.', '').replace(',', '.')
        try:
            return Decimal(value)
        except (TypeError, ValueError, Decimal.InvalidOperation):
            raise forms.ValidationError(self.error_messages['invalid'], code='invalid')

class ProdukForm(forms.ModelForm):
    harga_modal = ThousandsSeparatorDecimalField(widget=ThousandsSeparatorNumberInput)
    harga_jual = ThousandsSeparatorDecimalField(widget=ThousandsSeparatorNumberInput)

    class Meta:
        model = Produk
        fields = '__all__'

        
class JenisForm(forms.ModelForm):
    class Meta:
        model = Jenis
        fields = ['nama_jenis']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['nama_provider']

class JenisProviderForm(forms.ModelForm):
    class Meta:
        model = JenisProvider
        fields = ['jenis', 'provider']

class PulsaForm(forms.ModelForm):
    class Meta:
        model = Pulsa
        fields = ['saldo']  # Exclude 'tanggal_input' because it's non-editable
