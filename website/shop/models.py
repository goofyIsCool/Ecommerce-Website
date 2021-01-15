from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from PIL import Image
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


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default='S')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='P')
    slug = models.SlugField()
    description = models.TextField(
        default="To be, or not to be: that is the question: whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune, or to take arms against a")
    image = models.ImageField(default='default.jpg', upload_to='product_pics')

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 300:
            output_size = (500, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
