from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse    
from .models import Product , Category
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
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
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


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

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user in product.wishlist.all():
        product.wishlist.remove(request.user)
    else:
        product.wishlist.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def wishlist_view(request):
    products = request.user.wishlist_products.all()
    return render(request, 'products/wishlist.html', {'products': products})
