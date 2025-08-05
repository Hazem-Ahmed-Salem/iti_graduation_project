from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from products.models import Product

User = get_user_model()

class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def order_vat(self):
    #     return self.price_per_unit * self.quantity * Decimal(0.2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer.id,
            'product_id': self.product.id,
            # 'product_image': self.product.image.url,
            'product_name': self.product.name,
            'product_description': self.product.description,
            'product_category': self.product.category.name if self.product.category else None,
            'product_price': float(self.product.price),
            'quantity': self.quantity,
            'price_per_unit': float(self.price_per_unit),
            'order_price': (float(self.price_per_unit) * float(self.quantity)) ,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        return f"{self.customer}:{self.product}:{self.quantity} id:{self.id}"