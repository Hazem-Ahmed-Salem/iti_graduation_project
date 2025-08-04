from django.shortcuts import render


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return ('cart_detail')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return ('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    products = product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})

    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total': total})








# Create your views here.
