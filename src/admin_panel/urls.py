from django.urls import path
from .views import users_view,delete_user,add_user, products_view,product_detail, add_product, edit_product
from . import views
urlpatterns = [
    path('users/',users_view,name='users'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/add/', add_user, name='add_user'),
    path('products/',products_view,name='products'),
    path('products/<int:pk>/',product_detail,name='product_info'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_admin_product'),
    path('products/<int:pk>/edit/', edit_product, name='edit_admin_product'),
    path('products/add/', add_product, name='add_admin_product'),
    path('All_Orders/', views.All_Orders,name="All_Orders"),
    path('Cancelled/', views.Cancelled,name="Cancelled"),
    path('Done/', views.Done,name="Done"),
    path("Delete_Order/<int:order_id>/",views.Delete_Order,name="Delete_Order"),
    #

]

