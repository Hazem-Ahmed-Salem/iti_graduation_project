from django.urls import path
from .views import customers_view,delete_customer,add_customer, products_view

urlpatterns = [
    path('customers/',customers_view,name='customers'),
    path('customers/delete/<int:customer_id>/', delete_customer, name='delete_customer'),
    path('customers/add/', add_customer, name='add_customer'),
    path('products/',products_view,name='products'),
]

