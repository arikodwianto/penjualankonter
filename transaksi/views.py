from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Transaksi, TransaksiPulsa
from .forms import TransaksiForm, TransaksiPulsaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pulsa, TransaksiPulsa
from .forms import TransaksiPulsaForm
from django.core.exceptions import ValidationError
import logging
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.timezone import now

logger = logging.getLogger(__name__)

def transaksi_list(request):
    transaksi_list = Transaksi.objects.all()  # Ambil semua transaksi
    form = TransaksiForm()  # Inisialisasi form transaksi
    
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            transaksi = form.save(commit=False)  # Buat instance transaksi dari form tapi belum disimpan
            produk = transaksi.produk  # Ambil produk dari transaksi
            jumlah = transaksi.jumlah  # Ambil jumlah dari transaksi
            
            if produk.jumlah_stok >= jumlah:  # Cek apakah stok mencukupi
                transaksi.save()  # Simpan transaksi
                messages.success(request, 'Transaksi berhasil ditambahkan!')
            else:
                messages.error(request, f'Stok produk {produk.nama_produk} tidak mencukupi!')
            return redirect('transaksi_list')
    
    # Hitung total transaksi dan total keuntungan
    total_transaksi = sum(transaksi.jumlah for transaksi in transaksi_list)
    total_keuntungan = sum(transaksi.hitung_margin() for transaksi in transaksi_list)
    
    context = {
        'transaksi_list': transaksi_list,
        'form': form,
        'total_transaksi': total_transaksi,
        'total_keuntungan': total_keuntungan,
    }
    
    return render(request, 'transaksi/transaksi_list.html', context)

    
def transaksi_pulsa_list(request):
    if request.method == 'POST':
        form = TransaksiPulsaForm(request.POST)
        if form.is_valid():
            jumlah = form.cleaned_data['jumlah']
            nomor_hp = form.cleaned_data['nomor_hp']

            try:
                with transaction.atomic():
                    # Mengunci baris Pulsa untuk mencegah transaksi bersamaan
                    pulsa = Pulsa.objects.select_for_update().filter(saldo__gte=jumlah).order_by('id').first()
                    
                    if pulsa is None:
                        messages.error(request, 'Tidak ada pulsa dengan saldo cukup.')
                        return redirect('transaksi_pulsa_list')

                    # Mengurangi saldo pulsa
                    pulsa.saldo -= jumlah
                    pulsa.save()

                    # Menyimpan transaksi pulsa
                    transaksi_pulsa = form.save(commit=False)
                    transaksi_pulsa.pulsa = pulsa
                    transaksi_pulsa.nomor_hp = nomor_hp
                    transaksi_pulsa.save()
                    
                    messages.success(request, 'Transaksi pulsa berhasil dibuat.')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan: {str(e)}')

            return redirect('transaksi_pulsa_list')

    else:
        form = TransaksiPulsaForm()

    transaksi_pulsa_list = TransaksiPulsa.objects.all()
    total_transaksi = sum(transaksi.jumlah for transaksi in transaksi_pulsa_list)
    total_keuntungan = sum(transaksi.hitung_margin() for transaksi in transaksi_pulsa_list)

    context = {
        'transaksi_pulsa_list': transaksi_pulsa_list,
        'form': form,
        'total_transaksi': total_transaksi,
        'total_keuntungan': total_keuntungan,
    }
    return render(request, 'transaksi/transaksi_pulsa_list.html', context)





# Admin
def transaksi_list_admin(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaksi berhasil ditambahkan!')
            return redirect('transaksi_list_admin')
    else:
        form = TransaksiForm()

    transaksi_list = Transaksi.objects.all()
    total_transaksi = sum(transaksi.jumlah for transaksi in transaksi_list)
    total_keuntungan = sum(transaksi.hitung_margin() for transaksi in transaksi_list)

    context = {
        'transaksi_list': transaksi_list,
        'form': form,
        'total_transaksi': total_transaksi,
        'total_keuntungan': total_keuntungan,
    }
    return render(request, 'transaksi/transaksi_list_admin.html', context)

def transaksi_pulsa_list_admin(request):
    if request.method == 'POST':
        form = TransaksiPulsaForm(request.POST)
        if form.is_valid():
            jumlah = form.cleaned_data['jumlah']
            nomor_hp = form.cleaned_data['nomor_hp']

            # Ambil semua pulsa yang tersedia dan urutkan berdasarkan ID
            pulsa_list = Pulsa.objects.all().order_by('id')

            pulsa = None
            for p in pulsa_list:
                if p.saldo >= jumlah:
                    pulsa = p
                    break  # Temukan pulsa yang sesuai dan berhenti memeriksa yang lain

            if pulsa is None:
                messages.error(request, 'Tidak ada pulsa dengan saldo cukup.')
                return redirect('transaksi_pulsa_list_admin')

            # Simpan transaksi pulsa
            transaksi_pulsa = form.save(commit=False)
            transaksi_pulsa.pulsa = pulsa
            transaksi_pulsa.nomor_hp = nomor_hp
            try:
                transaksi_pulsa.save()
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('transaksi_pulsa_list_admin')

            # Kurangi saldo pulsa
            pulsa.saldo -= jumlah
            if pulsa.saldo <= 0:
                messages.success(request, f'Saldo pulsa {pulsa} habis, pulsa akan dihapus.')
                pulsa.delete()  # Hapus pulsa jika saldo sudah kosong
            else:
                pulsa.save()  # Simpan perubahan saldo

            messages.success(request, 'Transaksi pulsa berhasil dibuat.')
            return redirect('transaksi_pulsa_list_admin')
    else:
        form = TransaksiPulsaForm()

    transaksi_pulsa_list = TransaksiPulsa.objects.all()
    total_transaksi = sum(transaksi.jumlah for transaksi in transaksi_pulsa_list)
    total_keuntungan = sum(transaksi.hitung_margin() for transaksi in transaksi_pulsa_list)

    context = {
        'transaksi_pulsa_list': transaksi_pulsa_list,
        'form': form,
        'total_transaksi': total_transaksi,
        'total_keuntungan': total_keuntungan,
    }
    return render(request, 'transaksi/transaksi_pulsa_list_admin.html', context)