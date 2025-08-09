from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from user.models import Address
# from products.models import Product


User = get_user_model()

class Order(models.Model):
    Status_choices = [
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled'),
    ]
    payment_options=[
        ("cash_on_delivery","Cash on Delivery"),
        ("payment way","payment way"),
        ("vodafone cash","vodafone cash"),
        ("paypal","paypal"),
        ("Ebay","Ebay"),
        ("visa","visa")
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255,choices=Status_choices,default='confirmed')
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,default=None)
    payment_method = models.CharField(max_length=255,choices=payment_options,default='cash_on_delivery')
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.buyer}"

class Sale(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)  
    
    
    def __str__(self):
        return f"{self.order}"
