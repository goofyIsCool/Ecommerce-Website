from django.shortcuts import render
from .models import Product, OrderItem, Order, ShippingAddress, Category, Customer, Company
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages as messages
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
from django.utils import timezone
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home(request):
    try:
        data = cartData(request)
        counterCartItems = data['counterCartItems']
        cartItems = data['cartItems']
    except:
        counterCartItems = 0

    # Fix filtering recommended products
    recProdcuts = Product.objects.order_by('price')[:4]
    newProducts1 = Product.objects.order_by('-release_date')[:4]
    newProducts2 = Product.objects.order_by('-release_date')[4:8]
    categories = Category.get_all_categories()

    try:
        best = recProdcuts[0]
        context = {'cartItems': cartItems, 'categories': categories, 'best': best, 'newProducts1': newProducts1, 'newProducts2': newProducts2, 'recProducts': recProdcuts, 'counterCartItems': counterCartItems}
    except:
        context = {'categories': categories, 'newProducts1': newProducts1, 'newProducts2': newProducts2, 'recProducts': recProdcuts, 'counterCartItems': counterCartItems}

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

        cartItems = []
        try:
            data = cartData(self.request)
            counterCartItems = data['counterCartItems']
            cartItems = data['cartItems']
        except:
            counterCartItems = 0

        context['counterCartItems'] = counterCartItems
        context['current_category'] = " "
        categoryID = self.request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
            context['current_category'] = Category.objects.get(id=categoryID).name
        else:
            products = Product.get_all_products()

        categories = Category.get_all_categories()
        context['categories'] = categories
        context['filter'] = ProductFilterSet(self.request.GET, queryset=products)
        context['cartItems'] = cartItems

        return context


class ItemDetailView(DetailView):
    model = Product
    template_name = "shop/product.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        try:
            data = cartData(self.request)
            counterCartItems = data['counterCartItems']
            cartItems = data['cartItems']
            context['cartItems'] = cartItems
        except:
            counterCartItems = 0

        context['counterCartItems'] = counterCartItems
        categoryId = Category.objects.get(name=self.object.category.name)
        recProducts = Product.objects.filter(category=categoryId)
        context['recProducts'] = recProducts[:4]

        return context

# Make the generic Views login_required
class OrderListView(ListView):
    model = Order
    template_name = "shop/order_history.html"
    paginate_by = 10


    def get_queryset(self, *args, **kwargs):
        customer = self.request.user.customer
        queryset = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        try:
            data = cartData(self.request)
            counterCartItems = data['counterCartItems']
            cartItems = data['cartItems']
        except:
            counterCartItems = 0

        context['counterCartItems'] = counterCartItems
        context['cartItems'] = cartItems

        return context

class OrderProductsListView(ListView):
    model = OrderItem
    template_name = "shop/orders_products.html"

    def get_context_data(self, *args, **kwargs):

        try:
            data = cartData(self.request)
            counterCartItems = data['counterCartItems']
            cartItems = data['cartItems']
        except:
            counterCartItems = 0

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


    cartItems = []
    try:
        data = cartData(self.request)
        counterCartItems = data['counterCartItems']
        cartItems = data['cartItems']
    except:
        counterCartItems = 0

    context['counterCartItems'] = counterCartItems
    context['cartItems'] = cartItems

    return render(request, "shop/profile.html", context)


def cart(request):
    try:
        data = cartData(request)
        counterCartItems = data['counterCartItems']
        order = data['order']
        items = data['items']

        cartItems = data['cartItems']
        context = {'items': items, 'order': order, 'counterCartItems': counterCartItems}
        context['cartItems'] = cartItems

        return render(request, 'shop/cart.html', context)
    except:
        return render(request, 'shop/cart.html')


def checkout(request):
    try:
        data = cartData(request)
        counterCartItems = data['counterCartItems']
        order = data['order']
        items = data['items']
        cartItems = data['cartItems']

        context = {'items': items, 'order': order, 'counterCartItems': counterCartItems}
        context['cartItems'] = cartItems

        return render(request, 'shop/checkout.html', context)
    except:
        return render(request, 'shop/checkout.html')


def faq(request):
    try:
        data = cartData(request)
        counterCartItems = data['counterCartItems']
        cartItems = data['cartItems']

        context = {'cartItems': cartItems, 'counterCartItems': counterCartItems}
        return render(request, 'shop/FAQ.html', context)
    except:
        return render(request, 'shop/FAQ.html')


def about(request):
    try:
        data = cartData(request)
        counterCartItems = data['counterCartItems']
        cartItems = data['cartItems']

        context = {'cartItems': cartItems, 'counterCartItems': counterCartItems}
        return render(request, 'shop/about.html', context)
    except:
        return render(request, 'shop/about.html')


def contact(request):
    try:
        data = cartData(request)
        counterCartItems = data['counterCartItems']
        cartItems = data['cartItems']
        context = {'cartItems': cartItems, 'counterCartItems': counterCartItems}
        return render(request, 'shop/contact.html', context)
    except:
        return render(request, 'shop/contact.html')


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
            message = "Produkt został dodany do koszyka!"
        # elif action == 'remove':
        #     orderItem.quantity = (orderItem.quantity - orderItem.product.pack)
        #     message = "Produkty zosta!"
        elif action == 'removeAll':
            message = "Produkt został usunięty z twojego koszyka!"
            orderItem.quantity = 0
        elif action == 'update':
            message = "Produkt został zaktualizowany!"
            orderItem.quantity = quantity

        orderItem.save()  # saving it to store in database

        if orderItem.quantity <= 0:
            orderItem.delete()

        messages.success(request, message)
        return HttpResponse(order.get_cart_items) # Sending an success response

    return HttpResponse(order.get_cart_items)

def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    #całkowite
    całklowite = float(data['form']['total'][:-3])
    #grosze
    grosze = float(data['form']['total'][-2:])/100
    # total to w sumie z Vatem
    total = round(całklowite + grosze,2)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.transaction_id = transaction_id

    print(total)
    print(float(round(order.get_cart_total_brutto,2)))
    if total == float(round(order.get_cart_total_brutto,2)):
        order.complete = True
        order.total = decimal.Decimal(order.get_cart_total)
        order.vat = decimal.Decimal(order.get_cart_total_vat)
        order.brutto = round(decimal.Decimal(order.get_cart_total_brutto),2)
        order.date_ordered = timezone.localtime(timezone.now()).date()
        print("WORKING!")

    order.save()

    orderItems = OrderItem.objects.filter(order=order)
    # Company.objects.get_or_create(customer=customer)
    company, created  = Company.objects.get_or_create(customer=customer)
    if created:
        company.name = data['company']['name']
        company.nip = data['company']['nip']
        company.street = data['company']['street'],
        company.city = data['company']['city']
        company.zip_code = data['company']['zipcode']
        company.state = data['company']['state']
        company.country = data['company']['country']

    company.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        street=data['shipping']['street'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        country=data['shipping']['country'],
        zip_code=data['shipping']['zipcode'],
    )

    customer.name = data['form']['name']
    customer.surname = data['form']['surname']
    customer.email = data['form']['email']
    customer.phone = data['form']['phone']

    customer.save()

    current_site = get_current_site(request)
    mail_subject = 'Zamówienie Wólka Moda'
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

    # message = 'Please check your email. We've sent you an email with your order.'
    # context = {'messages': message}

    return JsonResponse('Payment complete!', safe=False)

def order_complete(request):
    return render(request,'shop/order_complete.html')

def moveItemCarts(request):

    print("OK!")
    device = request.COOKIES['device']
    customer1, created = Customer.objects.get_or_create(device=device) #Guest user
    customer2 = request.user.customer

    order1, created = Order.objects.get_or_create(customer=customer1, complete=False)
    order2, created = Order.objects.get_or_create(customer=customer2, complete=False)

    items1 = order1.orderitem_set.all()
    for item in items1:
        orderItem, created = OrderItem.objects.get_or_create(order=order2, product=item.product)
        orderItem.quantity = item.quantity

    order1.delete()

    return JsonResponse('We have succesfully moved your cart items!', safe=False)

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
            Q(title__contains=q) | Q(slug__icontains=q)
        ).distinct()

        for product in products:
            querySet.append(product)


    return list(set(querySet))


def confirmation(request):
    return render(request, 'shop/order_confirmation.html')


def regulamin(request):
    return render(request, 'shop/regulamin.html')
