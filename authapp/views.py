# authapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from .models import CustomUser
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.db.models import Sum
from stok.models import Produk, Pulsa
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Sum, F
from stok.models import Produk, Pulsa
from transaksi.models import Transaksi, TransaksiPulsa
from django.db.models.functions import TruncMonth

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authapp/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil! Selamat datang di sistem.')

            # Redirect user based on role
            if user.role == 'owner':
                return HttpResponseRedirect(reverse('owner_dashboard'))
            elif user.role == 'cashier':
                return HttpResponseRedirect(reverse('cashier_dashboard'))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Username atau password salah. Silakan coba lagi.')
    return render(request, 'authapp/login.html')

def home(request):
    return render(request, 'authapp/home.html')  # Tambahkan ini
def owner_home(request):
    
    return render(request, 'authapp/owner_home.html')  # Tambahkan ini

@login_required
def cashier_home(request):
    return render(request, 'authapp/cashier_home.html')  # Tambahkan ini

def owner_dashboard(request):
    today = now().date()  # Current date

    # Remaining stock
    sisa_stok = Produk.objects.aggregate(total_stok=Sum('jumlah_stok'))['total_stok'] or 0

    # Remaining pulsa balance
    sisa_pulsa = Pulsa.objects.aggregate(total_saldo=Sum('saldo'))['total_saldo'] or 0

    # Total revenue from product transactions today
    total_revenue_today = Transaksi.objects.filter(tanggal=today).aggregate(
        total_revenue=Sum(F('jumlah') * F('produk__harga_jual'))
    )['total_revenue'] or 0

    # Total quantity of products sold today
    total_sales_today = Transaksi.objects.filter(tanggal=today).aggregate(
        total_sales=Sum('jumlah')
    )['total_sales'] or 0

    # Total revenue from pulsa transactions today
    total_revenue_pulsa_today = TransaksiPulsa.objects.filter(tanggal=today).aggregate(
        total_revenue_pulsa=Sum('jumlah')
    )['total_revenue_pulsa'] or 0

    # Total quantity of pulsa sold today
    total_sales_pulsa_today = TransaksiPulsa.objects.filter(tanggal=today).aggregate(
        total_sales_pulsa=Sum('jumlah')
    )['total_sales_pulsa'] or 0

    # Monthly sales data aggregation
    monthly_sales = Transaksi.objects.annotate(month=TruncMonth('tanggal')).values('month').annotate(
        total_revenue=Sum(F('jumlah') * F('produk__harga_jual'))
    ).order_by('month')

    monthly_sales_data = {
        'months': [entry['month'].strftime('%B %Y') for entry in monthly_sales],
        'revenues': [entry['total_revenue'] for entry in monthly_sales]
    }

    context = {
        'sisa_stok': sisa_stok,
        'sisa_pulsa': sisa_pulsa,
        'total_revenue_today': total_revenue_today,
        'total_sales_today': total_sales_today,
        'total_revenue_pulsa_today': total_revenue_pulsa_today,
        'total_sales_pulsa_today': total_sales_pulsa_today,
        'monthly_sales_data': monthly_sales_data,
    }

    return render(request, 'authapp/owner_home.html', context)

# Admin
def home(request):
    today = now().date()

    # Calculate remaining stock
    sisa_stok = Produk.objects.aggregate(total_stok=Sum('jumlah_stok'))['total_stok'] or 0

    # Calculate remaining pulsa balance
    sisa_pulsa = Pulsa.objects.aggregate(total_saldo=Sum('saldo'))['total_saldo'] or 0

    # Calculate total revenue from product transactions today
    total_revenue_today = Transaksi.objects.filter(tanggal__date=today).aggregate(
        total_revenue=Sum(F('jumlah') * F('produk__harga_jual'))
    )['total_revenue'] or 0

    # Calculate total quantity of products sold today
    total_sales_today = Transaksi.objects.filter(tanggal__date=today).aggregate(
        total_sales=Sum('jumlah')
    )['total_sales'] or 0

    # Calculate total revenue from pulsa transactions today
    total_revenue_pulsa_today = TransaksiPulsa.objects.filter(tanggal__date=today).aggregate(
        total_revenue_pulsa=Sum('jumlah')
    )['total_revenue_pulsa'] or 0

    # Calculate total quantity of pulsa sold today
    total_sales_pulsa_today = TransaksiPulsa.objects.filter(tanggal__date=today).aggregate(
        total_sales_pulsa=Sum('jumlah')
    )['total_sales_pulsa'] or 0

    # Calculate monthly sales data
    monthly_sales = Transaksi.objects.annotate(month=TruncMonth('tanggal')).values('month').annotate(
        total_revenue=Sum(F('jumlah') * F('produk__harga_jual'))
    ).order_by('month')

    monthly_sales_data = {
        'months': [entry['month'].strftime('%B %Y') for entry in monthly_sales],
        'revenues': [entry['total_revenue'] for entry in monthly_sales]
    }

    context = {
        'sisa_stok': sisa_stok,
        'sisa_pulsa': sisa_pulsa,
        'total_revenue_today': total_revenue_today,
        'total_sales_today': total_sales_today,
        'total_revenue_pulsa_today': total_revenue_pulsa_today,
        'total_sales_pulsa_today': total_sales_pulsa_today,
        'monthly_sales_data': monthly_sales_data,
    }

    return render(request, 'authapp/home.html', context)

# Admin

@login_required
def cashier_dashboard(request):
    return render(request, 'authapp/cashier_home.html')
def profile(request):
    return render(request, 'authapp/profile.html')
@require_POST
def logout(request):
    auth_logout(request)
    return redirect('login') 
def custom_logout(request):
    logout(request)
    return redirect('login')

