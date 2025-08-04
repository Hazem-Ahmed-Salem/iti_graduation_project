from django.urls import path
from . import views

urlpatterns = [
    
    path('products/', views.product_list, name='product_list'),
    path('my-orders/', views.my_orders, name='my_orders'),   
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),



]