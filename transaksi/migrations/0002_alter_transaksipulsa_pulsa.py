# Generated by Django 5.0.3 on 2024-09-17 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stok', '0002_pulsatotal'),
        ('transaksi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaksipulsa',
            name='pulsa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaksi_pulsas', to='stok.pulsa'),
        ),
    ]
