# Generated by Django 3.2.2 on 2021-06-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20210617_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]