from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product
from orders.models import Order
from django.db.models import Sum

# التحقق إن المستخدم بائع
def is_seller(user):
    return user.is_authenticated and hasattr(user, 'is_seller') and user.is_seller

@login_required
@user_passes_test(is_seller)
def dashboard_view(request):
    # منتجات البائع
    products = Product.objects.filter(seller=request.user)

    # الطلبات على منتجاته
    orders = Order.objects.filter(product__seller=request.user)

    # بيانات الرسوم
    sales = orders.values('product__name').annotate(total_quantity=Sum('quantity'))
    labels = [item['product__name'] for item in sales]
    data = [item['total_quantity'] for item in sales]

    return render(request, 'seller_dashboard/dashboard.html',context= {
        'products': products,
        'orders': orders,
        'labels': labels,
        'data': data,
    })
