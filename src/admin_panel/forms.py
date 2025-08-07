from django import forms
from products.models import Product, Stock
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from user.models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'user_role', 'password']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


from .models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['seller', 'name', 'category', 'description', 'price', 'image', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['seller'].queryset = User.objects.filter(user_role='seller')


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantity']