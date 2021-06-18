# Generated by Django 3.2.2 on 2021-06-18 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210618_1439'),
        ('order', '0017_orderhistory_checksum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='OrderHistory',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.vendor'),
        ),
    ]
