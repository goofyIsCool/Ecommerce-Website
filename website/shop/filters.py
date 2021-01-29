from . models import Product
import django_filters
from django_filters.filters import RangeFilter

# Creating product filters


class ProductFilterSet(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'Ascending'), ('descending', 'Descending')
    )

    title = django_filters.CharFilter(lookup_expr='icontains')
    price = RangeFilter()
    ordering = django_filters.ChoiceFilter(
        label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Product
        fields = ['title', 'price', 'category']

    def filter_by_order(self, queryset, price, value):
        expression = 'price' if value == 'ascending' else '-price'
        return queryset.order_by(expression)
