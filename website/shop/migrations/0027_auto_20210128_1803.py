# Generated by Django 3.1.3 on 2021-01-28 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_auto_20210128_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='label',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('XS', 'extra small'), ('S', 'small'), ('M', 'medium'), (
                'L', 'large'), ('XL', 'extra large'), ('XXL', 'extra extra large')], default='S', max_length=3),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('S', 'Sukienki'), ('K', 'Koszule'),
                                            ('Sp', 'Spódniczki'), ('Ż', 'Żakiety')], default='S', max_length=2),
        ),
    ]