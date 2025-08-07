# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product,Category,Stock
from django.http import HttpResponse
from django.shortcuts import render
import os
import importlib.util
from django.conf import settings
from django.core.paginator import Paginator
from .forms import UserRegistrationForm , ProductForm,StockForm
from .models import User
from django.contrib import messages

    
def users_view(request):
    users = User.objects.all()
    return render(request, 'admin_panel/users.html', {'users': users})


def delete_user(request, user_id):
    users = User.objects.all()
    user_obj = get_object_or_404(users, id=user_id)
    user_obj.delete()
    return redirect('users')



def add_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserRegistrationForm()

    return render(request, 'admin_panel/add_user.html', {'form': form})

def products_view(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    return render(request, 'admin_panel/products.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'admin_panel/product_info.html', {
        'product': product
    })
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products')

def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        stock_form = StockForm(request.POST)
        if product_form.is_valid() and stock_form.is_valid():
            product = product_form.save(commit=False)
            stock = stock_form.save(commit=False)

            product.seller = User.objects.filter(user_role='seller').first()
            product.save()

            if product.image:
                product.URL_image = product.image.url
                product.save()

            stock.product = product
            stock.save()

            return redirect('products')
    else:
        product_form = ProductForm()
        stock_form = StockForm()
    return render(request, 'admin_panel/product_form.html', {'product_form': product_form, 'stock_form': stock_form})
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    stock = get_object_or_404(Stock, product=product)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        stock_form = StockForm(request.POST, instance=stock)
        if product_form.is_valid() and stock_form.is_valid():
            product = product_form.save()
            stock_form.save()

            if product.image:
                product.URL_image = product.image.url
                product.save()

            return redirect('product_info', pk=product.pk)
    else:
        product_form = ProductForm(instance=product)
        stock_form = StockForm(instance=stock)

    return render(request, 'admin_panel/product_form.html', {'product_form': product_form, 'stock_form': stock_form})


# def Dashboard(request):
#     return render(request,"admin_panel_templates/dashboard.html")


# def display_Electronic_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Electronic products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})


# def display_Kitchen_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Kitchen products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})





# def display_Beauty_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Beauty products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})




# def display_Makeup_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Makeup products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})





# def Orders(request):
#     Orders=order.objects.all()

#     paginator = Paginator(Orders,4) 
#     page_number = request.GET.get('page')
#     OrdersList = paginator.get_page(page_number)

    
#     return render(request,"admin_panel_templates/orders.html",{"OrdersList":OrdersList})



# def Recommendation(request):
#     return render(request,"admin_panel_templates/recommendation.html")




# def Cancelled(request):
#     OrdersList=order.objects.all()


#     return render(request,"admin_panel_templates/cancelled.html",{"OrdersList":OrdersList})


# def Done(request):
#     Orders=order.objects.all()
#     paginator = Paginator(Orders,4) 
#     page_number = request.GET.get('page')
#     OrdersList = paginator.get_page(page_number)


#     return render(request,"admin_panel_templates/done orders.html",{"OrdersList":OrdersList})

