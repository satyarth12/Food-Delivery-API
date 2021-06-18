# Generated by Django 3.2.2 on 2021-06-16 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_customer_vendor'),
        ('order', '0006_auto_20210616_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order_User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.vendor'),
        ),
    ]