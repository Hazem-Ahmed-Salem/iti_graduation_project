# from django import forms
# from products.models import Product


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ["name", "description", "price","image"]
        # widgets = {
        #     "name": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Product Name"}
        #     ),
        #     "description": forms.Textarea(
        #         attrs={
        #             "class": "form-control",
        #             "placeholder": "Product Description",
        #             "rows": 4,
        #         }
        #     ),
        #     "price": forms.NumberInput(
        #         attrs={"class": "form-control", "placeholder": "Price in P.E"}
        #     ),
        #     "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        # }
        # labels = {
        #     "name": "Product Name",
        #     "description": "Product Description",
        #     "price": "Price in P.E",
        #     "image": "image",
        # }

from django import forms
from products.models import Product, Stock

class AddProductForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0, required=True, label="Quantity")
    price = forms.FloatField(min_value=1)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, seller=None, commit=True):
        product = super().save(commit=False)
        if seller is not None:
            product.seller = seller
        if commit:
            product.save()
            Stock.objects.create(product=product, quantity=self.cleaned_data['quantity'])
        return product

class EditProductForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0, required=False, label="Add Quantity")
    price = forms.FloatField(min_value=1)
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        product = super().save(commit=commit)
        quantity = self.cleaned_data.get('quantity')
        if quantity:
            # Append to stock as an additional entry
            Stock.objects.create(product=product, quantity=quantity)
        return product
