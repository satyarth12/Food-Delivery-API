# Generated by Django 3.2.2 on 2021-06-12 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0017_alter_kitchen_kitchen_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='about',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='kitchenadress',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]