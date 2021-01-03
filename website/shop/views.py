from django.shortcuts import render
from .models import Item
# Create your views here.


def home(request):
    return render(request, 'shop/home.html')


def faq(request):
    return render(request, 'shop/FAQ.html')


def contact(request):
    return render(request, 'shop/contact.html')


def products(request):
    return render(request, 'shop/products.html')


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, " .html", context)
