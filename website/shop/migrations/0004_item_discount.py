# Generated by Django 3.1.3 on 2021-01-08 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_item_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
