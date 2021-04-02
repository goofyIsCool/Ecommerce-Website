from django.shortcuts import render
from shop.models import Order, OrderItem, Customer, Product
from datetime import date
# Create your views here.


def dashboard(request):
    dailyOrderCounter = Order.objects.filter(date_ordered=date.today(), complete=False).count()
    context = {"dailyOrderCounter": dailyOrderCounter}
    return render(request, 'dashboard/dashboard-base.html', context)
