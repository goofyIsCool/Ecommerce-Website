from django.shortcuts import render
from .models import Item
from django.views.generic import ListView, DetailView
# Create your views here.


class HomeListView(ListView):
    model = Item
    template_name = "shop/home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "shop/product.html"


def faq(request):
    return render(request, 'shop/FAQ.html')


def contact(request):
    return render(request, 'shop/contact.html')


def product_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "shop/products.html", context)
