from .models import Order, Customer
from django.http import HttpResponse

def cartData(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    counterCartItems = order.get_amount_of_items_cart
    cartItems = order.get_cart_items

    return {'cartItems': cartItems, 'counterCartItems': counterCartItems, 'customer': customer, 'order': order, 'items':items}
