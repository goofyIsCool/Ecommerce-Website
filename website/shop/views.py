from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'shop/home.html')


def faq(request):
    return render(request, 'shop/FAQ.html')


def contact(request):
    return render(request, 'shop/contact.html')


def products(request):
    return render(request, 'shop/products.html')
