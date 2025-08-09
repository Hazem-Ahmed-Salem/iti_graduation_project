from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from products.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal


# def add_to_cart(request, product_id):
#     cart = request.session.get('cart', {})
#     cart[str(product_id)] = cart.get(str(product_id), 0) + 1
#     request.session['cart'] = cart
#     return redirect ('cart_detail')

"""انا الي غيرت و عملت الفانكشان دي عشان تضيف منتج جديد في الكارت"""
@api_view(["POST"])
def add_to_cart(request):
    user = request.user if request.user.is_authenticated else None
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not user:
        return Response({'error': 'Authentication required.'}, status=401)

    if not product_id:
        return Response({'error': 'Product ID is required.'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=404)

    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'error': 'Quantity must be a positive integer.'}, status=400)

    cart_item, created = CartItem.objects.get_or_create(
        customer=user,
        product=product,
        defaults={
            'quantity': quantity,
            'price_per_unit': product.price,
            'order_price': Decimal(product.price) * quantity
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.price_per_unit = product.price
        cart_item.order_price = Decimal(cart_item.price_per_unit) * cart_item.quantity
        cart_item.save()

    return Response({
        'success': True,
        'cart_item_id': cart_item.id,
        'product': product.name,
    })

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



@login_required
def remove_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, customer=request.user)
    except CartItem.DoesNotExist:
        return redirect('shopping_cart')

    cart_item.delete()
    return redirect('shopping_cart')






