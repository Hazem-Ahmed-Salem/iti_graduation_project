from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse    
from .models import Product , Category
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
                URL_image=product['images'][0],
                is_featured=True,
                
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
    products = Product.objects.filter(is_featured=True)
    categories = Category.objects.filter(is_published=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = [p for p in products if p.get_stock_status()]

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'query': query,
        'in_stock': in_stock,
    }

    return render(request, 'products/product_list.html', context)



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

@api_view(['POST'])
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)
        return Response({'success':"item has been removed from wishlist",'wishlist_count': product.wishlist.count()},status=200)
    else:
        product.wishlist.add(request.user)
        return Response({'success':"item has been added from wishlist", 'wishlist_count': product.wishlist.count()},status=200)

   


@login_required
def wishlist_view(request):
    products = request.user.wishlist_products.all()
    return render(request, 'products/wishlist.html', {'products': products})

