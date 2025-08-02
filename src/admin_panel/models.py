from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    join_date = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1)

    def __str__(self):
        return self.name
