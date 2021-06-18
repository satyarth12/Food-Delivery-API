# Generated by Django 3.2.2 on 2021-06-18 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210618_1439'),
        ('moredata', '0012_auto_20210618_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refer_earn_customer',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refer_earn', to='account.customer'),
        ),
        migrations.AlterField(
            model_name='refer_earn_vendor',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refer_earn', to='account.vendor'),
        ),
    ]