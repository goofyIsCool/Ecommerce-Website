from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
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


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the ordered
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect("shop:product", slug=slug)
