from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='shop-home'),
    path('faq/', views.faq, name='shop-faq'),
    path('contact/', views.contact, name='shop-contact'),
    path('products/', views.products, name='shop-products'),
]
