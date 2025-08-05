from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

category_options=[



        ("select category","select category"),
        ("Electronic Products","Electronic Products"),
        ("Beauty Products","Beauty Products"),
        ("Kitchen Products","Kitchen Products"),
        ("Makeup Products","Makeup Products")

    ]

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/',null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    URL_image = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    wishlist = models.ManyToManyField(User, related_name='wishlist_products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_category_choices(cls):
        return Category.objects.filter(is_published=True)
    
    def get_stock_quantity(self):
        return Stock.objects.filter(product=self.id).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
    
    def get_stock_status(self):
        return self.get_stock_quantity() > 0
    
    def __str__(self):
        return self.name
    

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product}:{self.quantity} Units".title()
