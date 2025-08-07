from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price","image"]
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
