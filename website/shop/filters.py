from . models import Product
import django_filters
from django_filters.filters import RangeFilter

# Creating product filters


class ProductFilterSet(django_filters.FilterSet):
    CHOICES = (
        ('ascending', 'Ascending'), ('descending', 'Descending')
    )
    ordering = django_filters.ChoiceFilter(
        label='Ordering', choices=CHOICES, method='filter_by_order')
    # price = RangeFilter()

    class Meta:
        model = Product
        fields = ['category']

    def filter_by_order(self, queryset, price, value):
        expression = 'price' if value == 'ascending' else '-price'
        return queryset.order_by(expression)
