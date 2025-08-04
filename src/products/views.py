from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse    
from .models import Product , Category
import requests
# Create your views here.

def insert_product(request):
    response = requests.get('https://dummyjson.com/products')
    products = response.json()["products"] 
    try:
        for product in products:
            
            Product.objects.create(
                name=product['title'],
                description=product['description'],
                price=product['price'],
                stock=product['stock'],
                image=product['images'][0],
                is_featured=product.get('isFeatured', False),
                
            )
    except Exception as e:
        return HttpResponse(f"An error occurred {e}")
    return HttpResponse("Products inserted successfully")


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.all()[:8]
 
    return render(request, 'products/home.html', {
        'categories': categories,
        'products': featured_products
    })

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products
    })

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {
        'product': product
    })

def category_products_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products
    })