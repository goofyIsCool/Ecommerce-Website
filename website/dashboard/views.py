from django.shortcuts import render
from shop.models import Order, OrderItem, Customer, Product
from datetime import date
from django.utils import timezone
from datetime import datetime
import pytz
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def home(request):
    today = datetime.now()
    daily = Order.objects.filter(date_ordered = timezone.localtime(timezone.now()).date(), complete=True)
    dailyOrderCounter = daily.count()
    MonthlyOrderCounter = Order.objects.filter(date_ordered__month = timezone.localtime(timezone.now()).date().month, date_ordered__year = timezone.localtime(timezone.now()).date().year, complete=True).count()
    dailyIncome = 0
    for income in daily:
        dailyIncome += income.get_cart_total_brutto

    print(dailyIncome)
    # print (dailyOrderCounter)
    # print (timezone.localtime(timezone.now()).date())
    # print(timezone.localtime(timezone.now()).date().month)
    context = {"dailyOrderCounter": dailyOrderCounter, "MonthlyOrderCounter": MonthlyOrderCounter, "dailyIncome": dailyIncome, "orders": daily}
    return render(request, 'dashboard/home.html', context)


class ListViewOrder(ListView):
    model = Order
    template_name = "dashboard/orders.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.filter(complete=True).order_by('-date_ordered')
        return queryset
