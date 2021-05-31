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

def moveItemCarts(request):
    try:
        device = request.COOKIES['device']
        customer1, created = Customer.objects.get_or_create(device=device) #Guest user

    customer2 = request.user.customer #Logged in user
    order1, created = Order.objects.get_or_create(customer=customer1, complete=False)
    order2, created = Order.objects.get_or_create(customer=customer2, complete=False)

    items1 = order1.orderitem_set.all()
    for item in items1:
        orderItem, created = OrderItem.objects.get_or_create(order=order2, product=item.product)
        orderItem.quantity = item.quantity

    order1.delete()

    return "We have moved your cart items to your account"
