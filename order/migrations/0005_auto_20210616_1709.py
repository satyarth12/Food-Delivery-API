# Generated by Django 3.2.2 on 2021-06-16 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customer_vendor'),
        ('order', '0004_orderhistory_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='delivery',
            field=models.BooleanField(default=False, null=True, verbose_name='Out for delivery'),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='order_status',
            field=models.CharField(choices=[('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='ACCEPTED', max_length=50, verbose_name='Order Status from Vendor'),
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.vendor'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order_User', to='order.order'),
        ),
    ]