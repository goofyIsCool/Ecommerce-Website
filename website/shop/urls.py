from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('guest/', auth_views.LoginView.as_view(template_name='shop/guestUserLogin.html'), name='guest'),
    path('shipping_update/', views.shipping_update, name='shipping_update'),
]
