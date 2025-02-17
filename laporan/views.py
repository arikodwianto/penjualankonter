from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO, StringIO
import pandas as pd
from stok.models import Produk, Pulsa
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
import datetime
from django.db.models import Sum
from datetime import datetime
from transaksi.models import Transaksi, TransaksiPulsa

def produk_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        produk_list = Produk.objects.filter(transaksi__tanggal__range=[start_date, end_date]).distinct()
    else:
        produk_list = Produk.objects.all()

    return render(request, 'laporan/produk_report.html', {'produk_list': produk_list})

def pulsa_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        pulsa_list = Pulsa.objects.filter(tanggal_input__range=[start_date, end_date])
    else:
        pulsa_list = Pulsa.objects.all()

    return render(request, 'laporan/pulsa_report.html', {'pulsa_list': pulsa_list})

def export_produk_to_excel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        produk_list = Produk.objects.filter(transaksi__tanggal__range=[start_date, end_date]).distinct()
    else:
        produk_list = Produk.objects.all()

    html_string = render_to_string('laporan/template_produk.html', {'produk_list': produk_list})
    df = pd.read_html(StringIO(html_string))[0]

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Produk Report')
    writer.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="produk_report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
    return response

def export_pulsa_to_excel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        pulsa_list = Pulsa.objects.filter(tanggal_input__range=[start_date, end_date])
    else:
        pulsa_list = Pulsa.objects.all()

    html_string = render_to_string('laporan/template_pulsa.html', {'pulsa_list': pulsa_list})
    df = pd.read_html(StringIO(html_string))[0]

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Pulsa Report')
    writer.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="pulsa_report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
    return response

def laporan_home(request):
    return render(request, 'laporan/laporan_home.html')

def transaksi_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        transactions = Transaksi.objects.filter(tanggal__range=[start_date, end_date])
    else:
        transactions = Transaksi.objects.all()

    total_margin = transactions.aggregate(total_margin=Sum('jumlah'))['total_margin']
    return render(request, 'laporan/transaksi_report.html', {'transactions': transactions, 'total_margin': total_margin})


def transaksi_pulsa_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        transactions = TransaksiPulsa.objects.filter(tanggal__range=[start_date, end_date])
    else:
        transactions = TransaksiPulsa.objects.all()

    total_margin = transactions.count() * 2000
    return render(request, 'laporan/transaksi_pulsa_report.html', {'transactions': transactions, 'total_margin': total_margin})


def export_transaksi_to_excel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        transactions = Transaksi.objects.filter(tanggal__range=[start_date, end_date])
    else:
        transactions = Transaksi.objects.all()

    html_string = render_to_string('laporan/template_transaksi.html', {'transactions': transactions})
    df = pd.read_html(StringIO(html_string))[0]

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Transaksi Report')
    writer.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="transaksi_report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
    return response


def export_transaksi_pulsa_to_excel(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        transactions = TransaksiPulsa.objects.filter(tanggal__range=[start_date, end_date])
    else:
        transactions = TransaksiPulsa.objects.all()

    html_string = render_to_string('laporan/template_transaksi_pulsa.html', {'transactions': transactions})
    df = pd.read_html(StringIO(html_string))[0]

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Transaksi Pulsa Report')
    writer.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="transaksi_pulsa_report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
    return response