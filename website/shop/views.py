from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .forms import ShippingUpdateForm
import json
# Create your views here.


class HomeListView(ListView):
    model = Item
    template_name = "shop/home.html"
    paginate_by = 6

    ordering = ['date_added']


class ItemDetailView(DetailView):
    model = Item
    template_name = "shop/product.html"


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Your cart is empty")
            return redirect("/")


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
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated!")
            return redirect("shop:product", slug=slug)
        else:
            messages.info(request, "This item was added to your cart!")
            order.items.add(order_item)
            return redirect("shop:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart!")
        return redirect("shop:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("shop:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:product", slug=slug)


def checkout(request):
    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'shop/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Product:', productId)
    print('Action:', action)

    customer = request.user.customer
    product = Item.objects.get(id=productId)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required
def shipping_update(request):
    if request.method == 'POST':
        shipping_form = ShippingUpdateForm(request.POST, instance=request.user.customer)

        if shipping_form.is_valid():
            shipping_form.save()

            messages.success(
                request, f'Your account has been updated!')
            return redirect('shop:shipping_update')
    else:
        shipping_form = ShippingUpdateForm(instance=request.user.customer)

    context = {
        'shipping_form': shipping_form,
    }

    return render(request, 'shop/shipment.html', context)
