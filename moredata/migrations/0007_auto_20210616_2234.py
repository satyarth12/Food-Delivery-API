# Generated by Django 3.2.2 on 2021-06-16 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moredata', '0006_kitchenrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='kitchenrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='refer_earn',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='verified_kitchen',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
