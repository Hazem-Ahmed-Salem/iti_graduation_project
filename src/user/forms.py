from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile,Address


User = get_user_model()


class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    user_role = forms.ChoiceField(choices=[('customer', 'Customer'), ('seller', 'Seller')], required=True, label="Account Type")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, min_length=8)
    class Meta:
        model = User
        fields = ('first_name','last_name','email','user_role', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_role = self.cleaned_data['user_role']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['user_role'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['user_role'].choices = [('customer', 'Customer'),('seller', 'Seller')]
        self.fields['user_role'].widget.attrs['placeholder'] = 'Select Account Type'
        self.fields['user_role'].label = "Account Type"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['first_name'].widget.attrs['autofocus'] = True


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('email', 'password1')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].label = "Email"
        self.fields['password'].label = "Password"
        self.fields['email'].widget.attrs['autofocus'] = True



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'phone_number', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})

    def save(self,user, commit=True):
        profile = super().save(commit=False)
        profile.user = user
        profile.profile_picture = self.cleaned_data['profile_picture']
        profile.gender = self.cleaned_data['gender']
        profile.phone_number = self.cleaned_data['phone_number']

        if commit:
            profile.save()
        return profile
    
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'address', 'apartment', 'city', 'governorate']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['apartment'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['governorate'].widget.attrs.update({'class': 'form-control'})
        self.fields['address_type'].choices = [('home', 'Home'), ('work', 'Work'), ('other', 'Other')]
        self.fields['address_type'].label = "Address Type"
        self.fields['address'].label = "Address"
        self.fields['apartment'].label = "Apartment"
        self.fields['city'].label = "City"
        self.fields['governorate'].label = "Governorate"

    def save(self,user, commit=True):
        address = super().save(commit=False)
        address.user = user
        address.address_type = self.cleaned_data['address_type']
        address.address = self.cleaned_data['address']
        address.apartment = self.cleaned_data['apartment']
        address.city = self.cleaned_data['city']
        address.governorate = self.cleaned_data['governorate']
        if commit:
            address.save()
        return address
    
    