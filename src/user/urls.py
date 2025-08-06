from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('next_register/', views.next_register_view, name='next_register'),
    path('role_change/', views.request_role_change, name='request_role_change'),
    path('add_address/', views.add_address_view, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address_view, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
]


