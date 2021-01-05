from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='shop-home'),
    path('faq/', views.faq, name='shop-faq'),
    path('contact/', views.contact, name='shop-contact'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='shop-products'),
]
