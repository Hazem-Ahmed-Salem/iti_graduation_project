from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


def insert_product(request):
    response = requests.get("https://dummyjson.com/products")
    products = response.json()["products"]
    try:
        for product in products:
            Product.objects.create(
                name=product["title"],
                description=product["description"],
                price=product["price"],
                stock=product["stock"],
                image=product["images"][0],
                is_featured=product.get("isFeatured", False),
            )
    except Exception as e:
        return HttpResponse(f"An error occurred {e}")
    return HttpResponse("Products inserted successfully")


def home(request):
    return render(request, "home.html")


def product_list(request):
    return render(request, "product_list.html")


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        
    if form.is_valid():
            form.save()
            return redirect('seller_dashboard')

    return render(request, 'products/edit_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    product.delete()
    return redirect("seller_dashboard")


