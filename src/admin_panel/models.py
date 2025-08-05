from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    join_date = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1)

    def __str__(self):
        return self.name


#%%


# Create your models here.

class order(models.Model):

    payment_options=[
        ("payment way","payment way"),
        ("vodafone cash","vodafone cash"),
        ("paypal","paypal"),
        ("Ebay","Ebay"),
        (" visa",' visa')
    ]


    category_options=[



        ("select category","select category"),
        ("Electronic Products","Electronic Products"),
        ("Beauty Products","Beauty Products"),
        ("Kitchen Products","Kitchen Products"),
        ("Makeup Products","Makeup Products")

    ]
    
    name=models.TextField()

    image = models.URLField(blank=True, null=True)


    category=models.CharField(max_length=500,choices=category_options,default="select")

    customer_ID=models.CharField(max_length=6)

    address=models.CharField(max_length=1000)

    quantity=models.PositiveIntegerField(max_length=500)

    payment=models.CharField(max_length=100,choices=payment_options,default='select')

    cancelled=models.BooleanField(default=False)
    
    
















