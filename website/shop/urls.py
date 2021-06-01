from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from user import forms as user_forms

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<orderId>/', views.OrderProductsListView.as_view(), name='order'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/', views.addToCart, name='add_to_cart'),
    path('move_cart/', views.moveItemCarts, name='move_cart'),
    path('process_order/', views.processOrder, name='process_order'),
    path('guest/', auth_views.LoginView.as_view(template_name="shop/guestUserLogin.html", authentication_form=user_forms.UserLoginForm),name='guest'),
    path('shipping_update/', views.shipping_update, name='shipping_update'),
    path('order_confirmation/', views.confirmation, name='order_confirmation'),
    path('profile/', views.profile, name='profile'),
    path('regulamin/', views.regulamin, name='regulamin'),
]
