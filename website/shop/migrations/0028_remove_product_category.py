# Generated by Django 3.1.3 on 2021-01-31 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_auto_20210128_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
