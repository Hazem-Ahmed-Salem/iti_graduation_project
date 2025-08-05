from django.contrib import admin
# from .models import Customer
from . import models
from products.models import Product,Category


# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(models.order)

