from django.shortcuts import render
from django.http import HttpResponse    
from .models import Product
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
    return render(request, 'home.html')

def product_list(request):
    return render(request, 'product_list.html')