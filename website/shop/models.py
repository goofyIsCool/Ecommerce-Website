from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image
from django.utils import timezone
# Create your models here.

SIZE_CHOICES = (
    ('XS', 'extra small'),
    ('S', 'small'),
    ('M', 'medium'),
    ('L', 'large'),
    ('XL', 'extra large'),
    ('XXL', 'extra extra large')
)

PAYMENT_CHOICES = (
    ('d', 'delivery'),
    ('b', 'bank'),
)


class Customer(models.Model):
    name = models.CharField(default='', max_length=200)
    surname = models.CharField(default='', max_length=200)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(default='', max_length=20)
    nip = models.CharField(default='', max_length=20, null=True, blank=True)
    email = models.EmailField(null=False)

    def __str__(self):
        try:
            return (f'{self.user.username} Customer')
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
    slug = models.SlugField()
    description = models.TextField(
        default="", max_length=100)
    image1 = models.ImageField(default='default.jpg', upload_to='product_pics')
    image2 = models.ImageField(default='default.jpg', upload_to='product_pics')
    image3 = models.ImageField(default='default.jpg', upload_to='product_pics')
    image4 = models.ImageField(default='default.jpg', upload_to='product_pics')
    release_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'slug': self.slug,
        })

    def get_category_display(self):
        return self.category

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

        img = Image.open(self.image1.path)
        if img.width > 500 or img.height > 700:
            output_size = (500, 700)
            img.thumbnail(output_size)
            img.save(self.image1.path)

        img = Image.open(self.image2.path)
        if img.width > 500 or img.height > 700:
            output_size = (500, 700)
            img.thumbnail(output_size)
            img.save(self.image2.path)

        img = Image.open(self.image3.path)
        if img.width > 500 or img.height > 700:
            output_size = (500, 700)
            img.thumbnail(output_size)
            img.save(self.image3.path)

        img = Image.open(self.image4.path)
        if img.width > 500 or img.height > 700:
            output_size = (500, 700)
            img.thumbnail(output_size)
            img.save(self.image4.path)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment = models.CharField(choices=PAYMENT_CHOICES, max_length=1, default='d')

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    release_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=20, null=False)
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
