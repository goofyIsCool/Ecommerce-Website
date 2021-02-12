from django.shortcuts import render
from .models import Product, OrderItem, Order, ShippingAddress, Category
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import ShippingUpdateForm
import json
from .utils import cookieCart, cartData, guestOrder
import datetime
from .filters import ProductFilterSet
from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    recProdcuts = Product.objects.order_by('price')[:4]
    newProducts = Product.objects.order_by('-release_date')[:4]
    context = {'newProducts': newProducts, 'recProducts': recProdcuts, 'cartItems': cartItems}
    return render(request, 'shop/home.html', context)


class ProductListView(ListView):

    model = Product
    template_name = "shop/products.html"
    paginate_by = 16
    ordering = ['title']

    def get_queryset(self, *args, **kwargs):
        if 'q' in self.request.GET:
            query = self.request.GET['q']
            queryset = product_querySet(query)
            return queryset

        products = None
        categoryID = self.request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        queryset = ProductFilterSet(self.request.GET, queryset=products).qs
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(self.request)
            cartItems = cookieData['cartItems']

        context['current_category'] = " "
        categoryID = self.request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
            context['current_category'] = Category.objects.get(id=categoryID).name
        else:
            products = Product.get_all_products()

        context['cartItems'] = cartItems
        categories = Category.get_all_categories()
        context['categories'] = categories
        context['filter'] = ProductFilterSet(self.request.GET, queryset=products)
        return context


class ItemDetailView(DetailView):
    model = Product
    template_name = "shop/product.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(self.request)
            cartItems = cookieData['cartItems']

        context = super().get_context_data(**kwargs)
        context['cartItems'] = cartItems
        return context


class OrderListView(ListView):
    model = Order
    template_name = "shop/order_history.html"

    def get_queryset(self, *args, **kwargs):
        customer = self.request.user.customer
        queryset = Order.objects.filter(customer=customer, complete=True)

        return queryset


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'shop/checkout.html', context)


def faq(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'shop/FAQ.html', context)


def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'shop/contact.html', context)


def addToCart(request):
    if request.method == 'GET':
        productId = request.GET['productId']
        action = request.GET['action']
        quantity = int(request.GET['inputVal'])

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += quantity
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - orderItem.product.pack)
        elif action == 'removeAll':
            orderItem.quantity = 0

        orderItem.save()  # saving it to store in database

        if orderItem.quantity <= 0:
            orderItem.delete()

        return HttpResponse(order.get_cart_items)  # Sending an success response
    else:
        return HttpResponse(order.get_cart_items)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['inputVal']
    print('Action:', action)
    print('Product:', productId)
    print('Quantity:', quantity)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += quantity
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - orderItem.product.pack)
    elif action == 'removeAll':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if (request.user.is_authenticated):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        country=data['shipping']['country'],
        zip_code=data['shipping']['zipcode'],
    )
    return JsonResponse('Payment complete!', safe=False)


@ login_required
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


def product_querySet(query=None):
    querySet = []
    queries = query.split(" ")
    for q in queries:
        products = Product.objects.filter(
            Q(title__icontains=q),
        ).distinct()

        for product in products:
            querySet.append(product)

    return list(set(querySet))


def confirmation(request):
    return render(request, 'shop/order_confirmation.html')
