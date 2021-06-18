# Generated by Django 3.2.2 on 2021-05-27 18:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moredata', '0002_refer_earn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refer_earn',
            name='my_recommended_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
