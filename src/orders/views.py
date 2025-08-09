from django.shortcuts import render, redirect, get_object_or_404
from cart.models import CartItem
from .models import Order
from user.models import Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

@login_required
def user_orders_view(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', { 'orders': orders })

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'orders/order_detail.html', { 'order': order })

@login_required
def checkout_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(customer=user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('shopping_cart')

    addresses = Address.objects.filter(user=user)
    total = sum(item.order_price for item in cart_items)

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not selected_address_id or not payment_method:
            messages.error(request, "Please select both address and payment method.")
            return redirect('checkout')

        address = get_object_or_404(Address, id=selected_address_id, user=user)

        
        order = Order.objects.create(
            buyer=user,
            delivery_address=address,
            payment_method=payment_method,
        )

        products_data = []
        total_price = Decimal('0.00')
        for item in cart_items:
            if item.product.seller:
                seller = item.product.seller.to_dict
            else :
                seller =None
            item_data = {
                'seller_id': seller ,
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price_per_unit': float(item.price_per_unit),
                'order_price': float(item.order_price)
            }
            products_data.append(item_data)
            total_price += item.order_price

        order.products = products_data
        order.total_price = total_price
        order.save()

       
        cart_items.delete()

        messages.success(request, "Order placed successfully.")
        return redirect('receipt', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'total': total,
        'payment_options': Order.payment_options,
    })


@login_required
def receipt_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, buyer=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order does not exist.")
        return redirect('user_orders')
    return render(request, 'orders/receipt.html', {'order': order})





# # Create your views here.
