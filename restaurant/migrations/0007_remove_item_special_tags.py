# Generated by Django 3.2.2 on 2021-05-26 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_auto_20210525_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='special_tags',
        ),
    ]
