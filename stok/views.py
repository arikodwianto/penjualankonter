from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Produk, Jenis, Provider, JenisProvider, Pulsa
from .forms import ProdukForm, JenisForm, ProviderForm, JenisProviderForm, PulsaForm
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pulsa, PulsaTotal  # Ensure this is correct and not creating circular imports
from .forms import PulsaForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pulsa
from .forms import PulsaForm
from django.db.models import Sum


# Start Produk
def tambah_stok(request):
    if request.method == 'POST':
        produk_id = request.POST.get('produk')
        jumlah = request.POST.get('jumlah')

        try:
            produk = Produk.objects.get(id=produk_id)
            produk.jumlah_stok += int(jumlah)
            produk.save()
            messages.success(request, 'Stok berhasil ditambahkan.')
            return redirect('stok_list')
        except Produk.DoesNotExist:
            messages.error(request, 'Produk tidak ditemukan.')
            return redirect('stok_list')

    # No need for context if it's only handling POST requests in this case
    return redirect('stok_list')

def produk_tambah(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            nama_produk = form.cleaned_data['nama_produk']
            if Produk.objects.filter(nama_produk=nama_produk).exists():
                form.add_error('nama_produk', 'Produk dengan nama yang sama sudah ada.')
            else:
                form.save()
                messages.success(request, 'Produk berhasil ditambahkan.')
                return redirect('stok_list')
    else:
        form = ProdukForm()
    
    context = {
        'form': form,
        'jenis_providers': JenisProvider.objects.all(),
    }
    return render(request, 'stok/produk_tambah.html', context)


def produk_edit(request, produk_id):
    produk = get_object_or_404(Produk, id=produk_id)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diupdate.')
            return redirect('stok_list')
    else:
        form = ProdukForm(instance=produk)
    context = {
        'form': form,
    }
    return render(request, 'stok/produk_edit.html', context)

def produk_hapus(request, produk_id):
    if request.method == 'POST':
        produk = get_object_or_404(Produk, id=produk_id)
        produk.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def stok_list(request):
    produks = Produk.objects.all()
    total_produk = produks.count()
    total_modal = sum(produk.harga_modal for produk in produks)
    low_stock_products = produks.filter(jumlah_stok__lt=5)
    context = {
        'produks': produks,
        'total_produk': total_produk,
        'total_modal': total_modal,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'stok/stok_list.html', context)


# Admin

def tambah_stok_admin(request):
    if request.method == 'POST':
        produk_id = request.POST.get('produk')
        jumlah = request.POST.get('jumlah')

        try:
            produk = Produk.objects.get(id=produk_id)
            produk.jumlah_stok += int(jumlah)
            produk.save()
            messages.success(request, 'Stok berhasil ditambahkan.')
            return redirect('stok_list_admin')
        except Produk.DoesNotExist:
            messages.error(request, 'Produk tidak ditemukan.')
            return redirect('stok_list_admin')
    else:
        produks = Produk.objects.all()
        context = {
            'produks': produks,
        }
        return render(request, 'stok/stok_list_admin.html', context)

def stok_list_admin(request):
    produks = Produk.objects.all()
    total_produk = produks.count()
    total_modal = sum(produk.harga_modal for produk in produks)
    low_stock_products = produks.filter(jumlah_stok__lt=5)
    context = {
        'produks': produks,
        'total_produk': total_produk,
        'total_modal': total_modal,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'stok/stok_list_admin.html', context)
# End Produk

# Start Jenis
def tambah_jenis_inline(request):
    if request.method == 'POST':
        form = JenisForm(request.POST)
        if form.is_valid():
            nama_jenis = form.cleaned_data['nama_jenis']
            if Jenis.objects.filter(nama_jenis=nama_jenis).exists():
                form.add_error('nama_jenis', 'Nama jenis sudah ada.')
            else:
                form.save()
                messages.success(request, 'Jenis berhasil ditambahkan.')
                return redirect('jenis_list')
    else:
        form = JenisForm()
    
    return render(request, 'stok/jenis_list.html', {'form': form})

def jenis_list(request):
    if request.method == 'POST':
        form = JenisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis berhasil ditambahkan.')
            return redirect('jenis_list')
    else:
        form = JenisForm()
    
    jenis_list = Jenis.objects.all().order_by('-tanggal_input')
    return render(request, 'stok/jenis_list.html', {'form': form, 'jenis_list': jenis_list, 'edit_mode': False})

def edit_jenis(request, jenis_id):
    jenis = get_object_or_404(Jenis, id=jenis_id)
    if request.method == 'POST':
        form = JenisForm(request.POST, instance=jenis)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis berhasil diupdate.')
            return redirect('jenis_list')
    else:
        form = JenisForm(instance=jenis)
    
    jenis_list = Jenis.objects.all().order_by('-tanggal_input')
    return render(request, 'stok/jenis_list.html', {'form': form, 'jenis_list': jenis_list, 'edit_mode': True, 'edit_id': jenis_id})

def hapus_jenis(request, jenis_id):
    jenis = get_object_or_404(Jenis, id=jenis_id)
    
    if request.method == 'POST':
        jenis.delete()
        messages.success(request, 'Jenis berhasil dihapus.')
        return redirect('jenis_list')
    
    return redirect('jenis_list')
# End Jenis

# Start Provider
def tambah_provider(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            nama_provider = form.cleaned_data['nama_provider']
            if Provider.objects.filter(nama_provider=nama_provider).exists():
                form.add_error('nama_provider', 'Nama provider sudah ada.')
            else:
                form.save()
                messages.success(request, 'Provider berhasil ditambahkan.')
                return redirect('provider_list')
    else:
        form = ProviderForm()
    
    provider_list = Provider.objects.all().order_by('-tanggal_input')
    return render(request, 'stok/provider_list.html', {'form': form, 'provider_list': provider_list, 'edit_mode': False})

def provider_list(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Provider berhasil ditambahkan.')
            return redirect('provider_list')
    else:
        form = ProviderForm()
    
    provider_list = Provider.objects.all().order_by('-tanggal_input')
    return render(request, 'stok/provider_list.html', {'form': form, 'provider_list': provider_list, 'edit_mode': False})

def edit_provider(request, provider_id):
    provider = get_object_or_404(Provider, id=provider_id)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Provider berhasil diupdate.')
            return redirect('provider_list')
    else:
        form = ProviderForm(instance=provider)
    
    provider_list = Provider.objects.all().order_by('-tanggal_input')
    return render(request, 'stok/provider_list.html', {'form': form, 'provider_list': provider_list, 'edit_mode': True, 'edit_id': provider_id})

def hapus_provider(request, provider_id):
    if request.method == 'POST':
        try:
            provider = Provider.objects.get(id=provider_id)
            provider.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Provider.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Provider not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
# End Provider

# Start JenisProviders
def jenisprovider_list(request):
    if request.method == 'POST':
        form = JenisProviderForm(request.POST)
        if form.is_valid():
            jenis_id = form.cleaned_data['jenis']
            provider_id = form.cleaned_data['provider']
            
            if JenisProvider.objects.filter(jenis=jenis_id, provider=provider_id).exists():
                form.add_error('jenis', 'Jenis provider ini sudah terdaftar untuk provider yang dipilih.')
            else:
                form.save()
                messages.success(request, 'Jenis provider berhasil ditambahkan.')
                return redirect('jenisprovider_list')
    else:
        form = JenisProviderForm()
    
    jenisprovider_list = JenisProvider.objects.all()
    return render(request, 'stok/jenisprovider_list.html', {'form': form, 'jenisprovider_list': jenisprovider_list})

def tambah_jenisprovider(request):
    if request.method == 'POST':
        form = JenisProviderForm(request.POST)
        if form.is_valid():
            jenis_id = form.cleaned_data['jenis']
            provider_id = form.cleaned_data['provider']
            
            if JenisProvider.objects.filter(jenis=jenis_id, provider=provider_id).exists():
                form.add_error('jenis', 'Jenis provider ini sudah terdaftar untuk provider yang dipilih.')
            else:
                form.save()
                messages.success(request, 'Jenis provider berhasil ditambahkan.')
                return redirect('jenisprovider_list')
    else:
        form = JenisProviderForm()
    
    jenisprovider_list = JenisProvider.objects.all()
    return render(request, 'stok/jenisprovider_list.html', {'form': form, 'jenisprovider_list': jenisprovider_list})

def edit_jenisprovider(request, jenisprovider_id):
    jenisprovider = get_object_or_404(JenisProvider, id=jenisprovider_id)
    if request.method == 'POST':
        form = JenisProviderForm(request.POST, instance=jenisprovider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis provider berhasil diupdate.')
            return redirect('jenisprovider_list')
    else:
        form = JenisProviderForm(instance=jenisprovider)

    context = {
        'form': form,
        'jenisprovider': jenisprovider,
        'jenis_list': Jenis.objects.all(),
        'provider_list': Provider.objects.all(),
    }
    return render(request, 'stok/edit_jenisprovider.html', context)

def delete_jenisprovider(request, jenisprovider_id):
    jenisprovider = get_object_or_404(JenisProvider, id=jenisprovider_id)
    jenisprovider.delete()
    messages.success(request, 'Jenis provider berhasil dihapus.')
    return redirect('jenisprovider_list')
# End JenisProviders

# Start Pulsa
def pulsa_list(request):
    if request.method == 'POST':
        if 'add_pulsa' in request.POST:
            form = PulsaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Pulsa berhasil ditambahkan.')
                return redirect('pulsa_list')

    # Retrieve the list of pulsa and dynamically calculate total saldo
    pulsa_list = Pulsa.objects.all()
    
    # Calculate the total saldo by summing the saldo of all Pulsa objects
    total_saldo = pulsa_list.aggregate(total=Sum('saldo'))['total'] or 0

    # Initialize the form for adding new pulsa
    form = PulsaForm()

    context = {
        'pulsa_list': pulsa_list,
        'total_saldo': total_saldo,
        'form': form,
    }
    return render(request, 'stok/pulsa_list.html', context)
def pulsa_edit(request, pulsa_id):
    pulsa = get_object_or_404(Pulsa, id=pulsa_id)
    if request.method == 'POST':
        form = PulsaForm(request.POST, instance=pulsa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pulsa berhasil diupdate.')
            return redirect('pulsa_list')
    else:
        form = PulsaForm(instance=pulsa)
    
    context = {
        'form': form,
        'pulsa': pulsa,
        'edit_mode': True,
    }
    return render(request, 'stok/pulsa_list.html', context)

def pulsa_hapus(request, pulsa_id):
    pulsa = get_object_or_404(Pulsa, id=pulsa_id)
    if request.method == 'POST':
        pulsa.delete()
        messages.success(request, 'Pulsa berhasil dihapus.')
        return redirect('pulsa_list')
    
    context = {
        'pulsa': pulsa,
    }
    return render(request, 'stok/pulsa_hapus.html', context)

def tambah_saldo_pulsa(request, pulsa_id):
    pulsa = get_object_or_404(Pulsa, id=pulsa_id)

    if request.method == 'POST':
        jumlah_saldo = request.POST.get('jumlah_saldo', 0)
        if jumlah_saldo:
            pulsa.saldo += int(jumlah_saldo)
            pulsa.save()
            return redirect('pulsa_list')  # Redirect after successful update

    return redirect('pulsa_list')  # Redirect if the method is not POST


# Admin
def pulsa_list_admin(request):
    if request.method == 'POST':
        if 'add_pulsa' in request.POST:
            form = PulsaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Pulsa berhasil ditambahkan.')
                return redirect('pulsa_list_admin')  # Redirect to the same view
        elif 'edit_pulsa' in request.POST:
            pulsa_id = request.POST.get('pulsa_id')
            pulsa = get_object_or_404(Pulsa, id=pulsa_id)
            form = PulsaForm(request.POST, instance=pulsa)
            if form.is_valid():
                form.save()
                messages.success(request, 'Pulsa berhasil diupdate.')
                return redirect('pulsa_list_admin')  # Redirect to the same view

    pulsa_list = Pulsa.objects.all()  # Use consistent variable name
    total_pulsa = sum(pulsa.saldo for pulsa in pulsa_list)
    
    # Initialize form with empty or existing instance
    form = PulsaForm()
    
    context = {
        'pulsa_list': pulsa_list,  # Use consistent variable name
        'total_pulsa': total_pulsa,
        'form': form,
        'edit_mode': False,  # If you want to manage edit mode logic, you might need additional logic here
    }
    return render(request, 'stok/pulsa_list_admin.html', context)

# Admin

# End Pulsa
