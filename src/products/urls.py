from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('insert/', views.insert_product, name='insert_products'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('category/<int:pk>/', views.category_products_view, name='category_products'),
]
