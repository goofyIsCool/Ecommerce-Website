from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<orderId>/', views.OrderProductsListView.as_view(), name='orderAdmin'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
]
