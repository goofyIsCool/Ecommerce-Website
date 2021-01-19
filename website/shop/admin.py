from django.contrib import admin
from .models import Product, OrderItem, Order, Customer, ShippingAddress


# Register your models here.
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
