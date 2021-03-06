# Generated by Django 3.2.2 on 2021-06-03 21:05

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('restaurant', '0009_rename_name_kitchen_kitchen_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitchencuisine',
            name='cuisine_names',
            field=taggit.managers.TaggableManager(blank=True, help_text="What's the kitchen main cuisines? Not more than 10.", through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
