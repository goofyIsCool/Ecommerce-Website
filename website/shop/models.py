from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image
from django.utils import timezone
# Create your models here.

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('ST', 'T-Shirt'),
    ('SW', 'Sweatshirt'),
    ('J', 'Jeans'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(default='', max_length=20)
    nip = models.CharField(default='', max_length=20)

    def __str__(self):
        return f'{self.user.username} Customer'


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default='S')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='P')
    slug = models.SlugField()
    description = models.TextField(
        default="", max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'slug': self.slug,
        })

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.width > 500 or img.height > 700:
            output_size = (500, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # def get_total_item_price(self):
    #     return self.quantity*self.product.price
    #
    # def get_total_item_discount_price(self):
    #     return self.quantity*self.product.discount
    #
    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_item_discount_price()
    #
    # def get_final_price(self):
    #     if self.item.discount:
    #         return self.get_total_item_discount_price()
    #     return self.get_total_item_price()


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=20, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
