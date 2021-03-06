# Generated by Django 3.2.2 on 2021-06-17 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210618_0206'),
        ('moredata', '0008_auto_20210618_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refer_Earn_Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, max_length=12)),
                ('total_refer_money', models.IntegerField(blank=True, default=0, help_text='50 rs redeemed at each order.', null=True)),
                ('redeemed_money', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Refer_Earn_Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, max_length=12)),
                ('total_refer_money', models.IntegerField(blank=True, default=0, help_text='50 rs redeemed at each order.', null=True)),
                ('redeemed_money', models.IntegerField(blank=True, default=0, null=True)),
                ('my_recommended_users', models.ManyToManyField(blank=True, related_name='my_recommended_vendor', to='account.Vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Refer_Earn',
        ),
    ]
