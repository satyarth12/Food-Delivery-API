# Generated by Django 3.2.2 on 2021-06-18 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0012_auto_20210618_1645'),
        ('moredata', '0013_auto_20210618_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refer_earn_customer',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refer_earn', to='userinfo.customerprofile'),
        ),
        migrations.AlterField(
            model_name='refer_earn_vendor',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refer_earn', to='userinfo.vendorprofile'),
        ),
    ]
