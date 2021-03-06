# Generated by Django 3.2.2 on 2021-06-18 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moredata', '0011_auto_20210618_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refer_earn_customer',
            name='recommended_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by_customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='refer_earn_vendor',
            name='recommended_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by_vendor', to=settings.AUTH_USER_MODEL),
        ),
    ]
