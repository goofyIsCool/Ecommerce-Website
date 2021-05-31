from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image
from django.utils import timezone
import decimal
# Create your models here.

VAT = 0.23

SIZE_CHOICES = (
    ('XS', 'extra small'),
    ('S', 'small'),
    ('M', 'medium'),
    ('L', 'large'),
    ('XL', 'extra large'),
    ('XXL', 'extra extra large')
)

PAYMENT_CHOICES = (
    ('Przelewem', 'Przelewew'),
    ('Pobranie', 'Za Pobraniem'),
)


class Customer(models.Model):
    name = models.CharField(default='', max_length=200)
    surname = models.CharField(default='', max_length=200)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(default='', max_length=20)
    nip = models.CharField(default='', max_length=20, null=True, blank=True)
    email = models.EmailField(null=False)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        try:
            return (f'{self.user.username}')
        except:
            return 'Guest'


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Categories"

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=3, default='S')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    pack = models.IntegerField(default=0)
    slug = models.SlugField()
    description = models.TextField(
        default="", max_length=100)
    image1 = models.ImageField(default='default.jpg', upload_to='product_pics')
    image2 = models.ImageField(default='default.jpg', upload_to='product_pics')
    image3 = models.ImageField(default='default.jpg', upload_to='product_pics')
    release_date = models.DateTimeField(default=timezone.now)
    counter = models.IntegerField(default=0)  # licznik sprzedaży danego produktu

    def __str__(self):
        return self.title

    @staticmethod
    def get_netto_price(self):
        return self.price

    @property
    def get_brutto_price(self):
        return self.price*decimal.Decimal(1 + VAT)

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'slug': self.slug,
        })

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        images = [self.image1, self.image2, self.image3]
        for image in images:
            img = Image.open(image.path)
            if img.width > 400 or img.height > 600:
                output_size = (400, 600)
                img.thumbnail(output_size)
                img.save(image.path)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment = models.CharField(max_length=9, choices=PAYMENT_CHOICES, default='d')
    delivery = models.CharField(max_length=6, default='Kurier')
    total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    vat = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    brutto = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    comment = models.CharField(max_length=100, null=True, blank=True)
    Terms_and_conditions = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("shop:order", kwargs={
            'orderId': self.id,
        })

    @property
    def get_payment_name(self):
        return self.payment

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_total_vat(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total*decimal.Decimal(VAT)

    @property
    def get_cart_total_brutto(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total*decimal.Decimal(1 + VAT)

    # item quantity
    @property
    def get_amount_of_items_cart(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        arr = []
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            arr.append(item)

        return arr


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    release_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    @property
    def get_vat(self):
        total = self.product.price * self.quantity
        return total*decimal.Decimal(VAT)

    @property
    def get_brutto(self):
        total = self.product.price * self.quantity
        return total*decimal.Decimal(1 + VAT)

class Company(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    nip = models.CharField(max_length=10, null=False)
    street = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=20, null=False)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=20, null=False)

    def __str__(self):
        if self.customer.name == '':
            return "Guest: " + self.address
        else:
            return self.customer.name + ": " + self.address
