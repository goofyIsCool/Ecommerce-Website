from . models import Product
import django_filters
from django_filters.filters import RangeFilter
from django import forms

# Creating product filters


class ProductFilterSet(django_filters.FilterSet):
    CHOICES = (
        ('ascending_price', 'Rosnąco po cenie'), ('descending_price', 'Malejąco po cenie'), ('ascending_title', 'A-Z'), ('descending_title', 'Z-A')
    )
    ordering = django_filters.ChoiceFilter(
        label='Posortuj', choices=CHOICES, method='filter_by_order' )
    # price = RangeFilter()

    def filter_by_order(self, queryset, price, value):
        # expression = 'price' if value == 'ascending_price' else '-price'
        if value == 'ascending_price':
            expression = 'price'
        elif value == 'descending_price':
            expression = '-price'
        elif value == 'ascending_title':
            expression = 'title'
        elif value == 'descending_title':
            expression = '-title'

        return queryset.order_by(expression)
