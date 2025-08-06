from django import forms
from django.contrib.auth import get_user_model

from products.models import Product, Stock


User = get_user_model()

class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name'] 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_role = 'customer' 
        if commit:
            user.save()
        return user
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'is_featured']
        widgets = {
            'description': forms.Textarea(),
        }

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantity']