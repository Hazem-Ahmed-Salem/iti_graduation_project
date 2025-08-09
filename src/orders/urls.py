from django.urls import path
from . import views
from products.views import product_detail_view

urlpatterns = [
      # path('products/', product_detail_view, name='product_list'),
      path('my-orders/', views.user_orders_view, name='user_orders'),   
      path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
      path('checkout/', views.checkout_view, name='checkout'),
      path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),
      path("cancel/<int:order_id>",views.cancel_order,name="cancel")
]