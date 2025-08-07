from django.urls import path
from .views import users_view,delete_user,add_user, products_view,product_detail, add_product, edit_product
from . import views
urlpatterns = [
    path('users/',users_view,name='users'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/add/', add_user, name='add_user'),
    path('products/',products_view,name='products'),
    path('products/<int:pk>/',product_detail,name='product_info'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:pk>/edit/', edit_product, name='edit_product'),
    path('products/add/', add_product, name='add_product'),
    # path('Dashboard/', views.Dashboard,name="Dashboard"),
    # path('display_Electronic_products/', views.display_Electronic_products,name="display_Electronic_products"),
    # path('display_Kitchen_products/', views.display_Kitchen_products,name="display_Kitchen_products"),
    # path('display_Beauty_products/', views.display_Beauty_products,name="display_Beauty_products"),
    # path('display_Makeup_products/', views.display_Makeup_products,name="display_Makeup_products"),
    # path('Orders/', views.Orders,name="Orders"),
    # path('Cancelled/', views.Cancelled,name="Cancelled"),
    # path('Done/', views.Done,name="Done"),
    # path("Recommendation/",views.Recommendation,name="Recommendation")

]

