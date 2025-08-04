from django.urls import path
from . import views

urlpatterns = [
    
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),  # ← هنا الاسم
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
]

