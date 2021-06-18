# Generated by Django 3.2.2 on 2021-06-18 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210618_1439'),
        ('userinfo', '0010_auto_20210618_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='VendorProfile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.vendor'),
        ),
        migrations.AlterField(
            model_name='CustomerProfile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.customer'),
        ),
    ]