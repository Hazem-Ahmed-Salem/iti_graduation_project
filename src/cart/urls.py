from django.urls import path
from . import views
from products.views import product_detail_view
from products.models import Product

urlpatterns = [
    
      # path('products/', product_detail_view, name='product_list'),
      path('', views.cart_detail, name='shopping_cart'), 
#     path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
      path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
      path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
]

