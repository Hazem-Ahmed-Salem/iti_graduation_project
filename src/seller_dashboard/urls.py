from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('products/', views.my_products_view, name='my_products'),
    path('products/add/', views.add_product_view, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product_view, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product_view, name='delete_product'),
    path('orders/', views.my_orders_view, name='my_orders'),
    path('statistics/', views.sales_stats_view, name='sales_stats'),
]
