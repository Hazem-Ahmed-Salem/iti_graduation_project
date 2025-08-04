from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import OrderItem  # هنحتاج نجهزه
from products.forms import ProductForm
from django.http import JsonResponse
from django.db.models import Sum
import datetime





def dashboard_view(request):
    # total_products = Product.objects.filter(seller=request.user).count()
    # total_orders = OrderItem.objects.filter(product__seller=request.user).count()
    # total_sales = OrderItem.objects.filter(product__seller=request.user).aggregate(total=Sum('price'))['total'] or 0
    # context = {
    #     'total_products': total_products,
    #     'total_orders': total_orders,
    #     'total_sales': total_sales
    # }
    return render(request, 'seller_dashboard/dashboard.html')



def my_products_view(request):
    # products = Product.objects.filter(seller=request.user)
    return render(request, 'seller_dashboard/my_products.html')



def add_product_view(request):
    # form = ProductForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     product = form.save(commit=False)
    #     product.seller = request.user
    #     product.save()
    #     return redirect('seller_dashboard:my_products')
    return render(request, 'seller_dashboard/add_product.html')


def edit_product_view(request, pk):
    # product = get_object_or_404(Product, pk=pk, seller=request.user)
    # form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    # if form.is_valid():
    #     form.save()
    #     return redirect('seller_dashboard:my_products')
    return render(request, 'seller_dashboard/edit_product.html')


def delete_product_view(request, pk):
    # product = get_object_or_404(Product, pk=pk, seller=request.user)
    # if request.method == 'POST':
    #     product.delete()
    #     return redirect('seller_dashboard:my_products')
    return render(request, 'seller_dashboard/confirm_delete.html')



def my_orders_view(request):
    # orders = OrderItem.objects.filter(product__seller=request.user)
    return render(request, 'seller_dashboard/orders.html')



# def sales_stats_view(request):
    # today = datetime.date.today()
    # last_7_days = [today - datetime.timedelta(days=i) for i in range(7)]
    # data = []
    # for day in last_7_days[::-1]:
    #     day_total = OrderItem.objects.filter(
    #         product__seller=request.user,
    #         created_at__date=day
    #     ).aggregate(total=Sum('price'))['total'] or 0
    #     data.append({'date': day.strftime('%Y-%m-%d'), 'sales': float(day_total)})
    # return JsonResponse(data, safe=False)
