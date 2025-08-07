from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Address
from products.models import Product, Category
from .forms import RegisterationForm, LoginForm , UserProfileForm , AddressForm
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('next_register')
        else:
            error_message = form.errors.as_text()
            return render(request, 'user/register.html', {'form': RegisterationForm(), "errors": error_message})
    return render(request, 'user/register.html', {'form': RegisterationForm()})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if user.user_role == 'admin':
                    return redirect('customers')
                elif user.user_role == 'seller':
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                return render(request, 'user/login.html', {'form': form, 'errors': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def next_register_view(request):
    try:
        if request.user.profile:
            return redirect('profile')
    except ObjectDoesNotExist:
        pass
    profile_form = UserProfileForm()
    address_form = AddressForm()
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)
        if profile_form.is_valid() and address_form.is_valid():
            address_form.save(request.user)
            profile_form.save(request.user)
            return redirect('profile')
        else:
            return render(request, 'user/next_register.html', {'address_form': address_form,'profile_form':profile_form, 'errors': [address_form.errors, profile_form.errors]})
    return render(request, 'user/next_register.html',{'address_form': address_form,'profile_form':profile_form})


@login_required
def profile_view(request):
    try:
        Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        redirect('next_register')
    try:
        addresses = Address.objects.filter(user=request.user)
    except Address.DoesNotExist:
        redirect('next_register')
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        print(profile_picture)
        user_update_fields = {}
        profile_update_fields = {}
        if email:
            user_update_fields['email'] = email
        if first_name:
            user_update_fields['first_name'] = first_name
        if last_name:
            user_update_fields['last_name'] = last_name
        if user_update_fields:
            User.objects.filter(id=request.user.id).update(**user_update_fields)
        if profile_picture:
            profile_update_fields['profile_picture'] = profile_picture
        if gender:
            profile_update_fields['gender'] = gender
        if phone_number:
            profile_update_fields['phone_number'] = phone_number
        if profile_update_fields:
            profile = Profile.objects.filter(user=request.user).update(**profile_update_fields)

        
    return render(request, 'user/profile.html',{"addresses":addresses})

@api_view(['POST'])
def request_role_change(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    new_role = request.data.get('role')
    print(new_role )
    if new_role in ['seller', 'customer']:
        print(new_role )
        user.user_role = new_role
        user.save()
        return Response({'success': 'Role change requested successfully.'}, status=200)
    elif new_role == 'admin':
        if user.is_superuser:
            user.user_role = 'admin'
            user.save()
            return Response({'success': 'Role changed to admin successfully.'}, status=200)
    else:
        print(new_role )
        print(f"Invalid role: {new_role}")
        return Response({'error': 'Invalid role.'}, status=400)
    

@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('profile')
        else:
            return render(request, 'user/add_address.html', {'form': form, 'errors': form.errors})
    else:
        form = AddressForm()
    return render(request, 'user/add_address.html', {'form': form})

@login_required
def edit_address_view(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return redirect('profile')
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('profile')
        else:
            return render(request, 'user/edit_address.html', {'form': form, 'errors': form.errors.as_text()})
    else:
        form = AddressForm(instance=address)
    return render(request, 'user/edit_address.html', {'form': form})

@api_view(['DELETE'])
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        address.delete()
        return Response({'success': 'Address deleted successfully.'}, status=200)
    except Address.DoesNotExist:
        return Response({'error': 'Address not found.'}, status=404)