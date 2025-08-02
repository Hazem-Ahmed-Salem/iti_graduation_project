from django.urls import path
from . import views

urlpatterns = [
    path('seller_dashboard', views.dashboard_view, name='seller_dashboard'),
]
