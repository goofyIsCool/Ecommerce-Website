from .models import Order, Customer
import js2py
from django.http import HttpResponse


# def uuid():
#     arr = "function uuidv4() {
#         return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
#             var r=Math.random() * 16 | 0, v=c == 'x' ? r: (r & 0x3 | 0x8)
#             return v.toString(16)
#         })
#     }"
#
#     uuid_code = js2py.eval_js(arr)
#
#     return uuid_code()


# def setcookie(request):
#     response = HttpResponse("Cookie Set")
#     response.set_cookie('device', uuid())
#     return response
#
#
# def getcookie(request):
#     try:
#         device = request.COOKIES['device']
#     except:
#         setcookie(request)
#
#     device = request.COOKIES['device']
#     return {'device': device}


def cartData(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    return {'cartItems': cartItems, 'order': order, 'items': items, 'customer': customer, 'device': device}
