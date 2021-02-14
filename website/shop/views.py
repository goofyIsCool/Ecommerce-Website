from django.shortcuts import render
from .models import Product, OrderItem, Order, ShippingAddress, Category, Customer
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import ShippingUpdateForm, UserUpdateForm, ProfileUpdateForm
import json
from .utils import cartData
import datetime
from .filters import ProductFilterSet
from django.http import HttpResponse
import decimal
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    recProdcuts = Product.objects.order_by('price')[:4]
    newProducts = Product.objects.order_by('-release_date')[:4]

    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    context = {'newProducts': newProducts, 'recProducts': recProdcuts,
               'cartItems': cartItems, 'order': order}
    return render(request, 'shop/home.html', context)


class ProductListView(ListView):

    model = Product
    template_name = "shop/products.html"
    paginate_by = 8
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            customer = self.request.user.customer
        except:
            device = self.request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        context['current_category'] = " "
        categoryID = self.request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
            context['current_category'] = Category.objects.get(id=categoryID).name
        else:
            products = Product.get_all_products()

        context['order'] = order
        context['cartItems'] = cartItems
        categories = Category.get_all_categories()
        context['categories'] = categories
        context['filter'] = ProductFilterSet(self.request.GET, queryset=products)
        return context


class ItemDetailView(DetailView):
    model = Product
    template_name = "shop/product.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            customer = self.request.user.customer
        except:
            device = self.request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        context['cartItems'] = cartItems
        return context


class OrderListView(ListView):
    model = Order
    template_name = "shop/order_history.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        customer = self.request.user.customer
        queryset = Order.objects.filter(customer=customer, complete=True)

        return queryset


class OrderProductsListView(ListView):
    model = OrderItem
    template_name = "shop/orders_products.html"

    def get_context_data(self, *args, **kwargs):
        orderId = self.kwargs['orderId']
        order = Order.objects.get(id=orderId)
        orderItems = OrderItem.objects.filter(order=order)
        context = {'order': order, 'items': orderItems}
        return context


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.customer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('shop:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)

    user = request.user
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
    }

    return render(request, "shop/profile.html", context)


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

        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

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

    return HttpResponse(order.get_cart_items)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    total = float(data['form']['total'])
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.total = decimal.Decimal(order.get_cart_total)

    order.save()

    orderItems = OrderItem.objects.filter(order=order)

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        country=data['shipping']['country'],
        zip_code=data['shipping']['zipcode'],
    )

    current_site = get_current_site(request)
    mail_subject = 'Your Wólka Moda order.'
    message = render_to_string('shop/order_email.html', {
        'customer': customer,
        'domain': current_site.domain,
        'orderItems': orderItems,
        'order': order
    })
    to_email = customer.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()

    # message = 'Please check your email address to complete the registration'
    # context = {'messages': message}

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
