# Generated by Django 3.2.2 on 2021-06-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20210616_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='succes_at',
            field=models.DateTimeField(),
        ),
    ]
