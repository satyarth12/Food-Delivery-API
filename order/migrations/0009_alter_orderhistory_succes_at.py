# Generated by Django 3.2.2 on 2021-06-16 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_orderhistory_succes_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='succes_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
