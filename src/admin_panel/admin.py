from django.contrib import admin
from .models import Customer
from . import models
# Register your models here.
admin.site.register(Customer)

admin.site.register(models.order)