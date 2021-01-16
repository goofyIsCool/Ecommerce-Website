from django.contrib import admin
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
]
