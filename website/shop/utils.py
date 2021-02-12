import json
from .models import Product, Order, Customer, OrderItem
import decimal


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_total_brutto': 0,
             'get_cart_total_vat': 0, 'get_cart_items': 0}

    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * product.pack * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'image': product.image1.url,
                    'url': product.get_absolute_url,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total,
                'pack': product.pack,
            }
            items.append(item)
            order['get_cart_total_vat'] += total*decimal.Decimal(0.23)
            order['get_cart_total_brutto'] += total*decimal.Decimal(1.23)
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print("User is not logged in..")
    print("Cookies: ", request.COOKIES)
    name = data['form']['name']
    surname = data['form']['surname']
    phone = data['form']['phone']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email,)

    customer.name = name
    customer.surname = surname
    customer.phone = phone
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
