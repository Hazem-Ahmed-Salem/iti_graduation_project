from django.shortcuts import render, redirect , get_object_or_404
from .models import Order, OrderItem
from .forms import CheckoutForm
from products.models import Product
from django.contrib.auth.decorators import login_required




def checkout_view(request):
    cart = request.session.get('cart', {})  
    if not cart:
        return redirect('cart_detail') 

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                address=form.cleaned_data['address'],
                payment_method=form.cleaned_data['payment_method']
            )

            for pid, qty in cart.items():
                product = Product.objects.get(id=pid)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )

            
            request.session['cart'] = {}
            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def receipt_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/receipt.html', {'order': order})





# Create your views here.
