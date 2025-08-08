from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from products.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required
from decimal import Decimal


@login_required
def add_to_cart(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        customer=request.user,
        product=product,
        defaults={
            'quantity': 1,
            'price_per_unit': product.price,
            'order_price': product.price
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.order_price = cart_item.price_per_unit * cart_item.quantity
        cart_item.save()

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, product_id):
    
    cart_item = get_object_or_404(
        CartItem,
        customer=request.user,
        product_id=product_id
    )

    
    cart_item.delete()

    
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    
    cart_items = CartItem.objects.filter(customer=request.user)

    for item in cart_items:
        if item.price_per_unit == 0 or item.order_price == 0:
            item.price_per_unit = item.product.price
            item.order_price = item.price_per_unit * item.quantity
            item.save()

    
    total = sum(item.order_price for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })







