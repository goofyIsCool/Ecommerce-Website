from django.contrib import admin
from .models import Product, OrderItem, Order, Customer, ShippingAddress, Category
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}"width="75" height="75" />'.format(obj.image1.url))

    image_tag.short_description = 'Image'

    list_display = ['image_tag', 'title', 'category', 'pack', 'price']


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(Category)
