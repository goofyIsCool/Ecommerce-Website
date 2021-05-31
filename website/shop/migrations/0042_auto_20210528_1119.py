# Generated by Django 3.2.3 on 2021-05-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0041_product_counter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='street',
        ),
        migrations.RemoveField(
            model_name='order',
            name='message',
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='totalVat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]