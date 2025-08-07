from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from products.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect ('cart_detail')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect ('cart_detail')


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







