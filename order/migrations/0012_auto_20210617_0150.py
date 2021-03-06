# Generated by Django 3.2.2 on 2021-06-16 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20210616_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistory',
            name='future_date',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='future_time',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='is_future',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='review',
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='FutureOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_future', models.BooleanField(blank=True, default=False, null=True)),
                ('future_date', models.DateField(blank=True, help_text='Date selected for the future order', null=True)),
                ('future_time', models.TimeField(blank=True, help_text='Time Slot selected for the future order delivery', null=True)),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Future_Order', to='order.order')),
            ],
        ),
        migrations.AddField(
            model_name='orderhistory',
            name='for_future',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.futureorder'),
        ),
    ]
