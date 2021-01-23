from django.shortcuts import render
from .models import Product, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import ShippingUpdateForm
import json
# Create your views here.


def home(request):
    return render(request, 'shop/home.html')


class ProductListView(ListView):
    model = Product
    template_name = "shop/products.html"
    paginate_by = 12

    ordering = ['date_added']


class ItemDetailView(DetailView):
    model = Product
    template_name = "shop/product.html"


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'shop/checkout.html', context)


def faq(request):
    return render(request, 'shop/FAQ.html')


def contact(request):
    return render(request, 'shop/contact.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'removeAll':
        orderItem.quantity = 0

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
