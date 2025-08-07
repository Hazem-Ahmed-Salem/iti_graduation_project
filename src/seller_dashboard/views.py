from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Sum
import datetime
from products.models import Product
from orders.models import Sale  
from .forms import ProductForm
from django.http import JsonResponse
from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

###############################################


@login_required
def dashboard_view(request):
    seller = request.user

    # عدد المنتجات الخاصة بالبائع
    total_products = Product.objects.filter(seller=seller).count()

    # هات كل مبيعات النظام
    sales = Sale.objects.all()

    total_orders = 0
    total_sales = 0

    # IDs بتاعة المنتجات الخاصة بالبائع
    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )

    # مراجعة كل الطلبات
    for sale in sales:
        sale_has_product = False  # هنتأكد هل فيها منتجات للبائع ولا لأ

        for item in sale.products:  # sale.products = JSONField
            product_id = item.get("id")
            quantity = item.get("quantity", 1)
            price = item.get("price", 0)

            if product_id in seller_product_ids:
                sale_has_product = True
                total_sales += quantity * price

        if sale_has_product:
            total_orders += 1

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_sales": total_sales,
    }

    return render(request, "seller_dashboard/dashboard.html", context)


###############################################
@login_required
def my_products_view(request):
    seller = request.user
    products = Product.objects.filter(seller=seller)

    context = {"products": products}

    return render(request, "seller_dashboard/my_products.html", context)


###############################################
@login_required
def add_product_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # ربط المنتج بالبائع الحالي
            product.save()
            return redirect("seller_dashboard:my_products")
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "seller_dashboard/add_product.html", context)


###############################################
@login_required
def edit_product_view(request, pk):
    seller = request.user
    product = get_object_or_404(Product, pk=pk, seller=seller)  # تأكد إنه منتج البائع

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("seller_dashboard:my_products")
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "seller_dashboard/edit_product.html", context)


###############################################
@login_required
def delete_product_view(request, pk):
    seller = request.user
    product = get_object_or_404(Product, pk=pk, seller=seller)

    if request.method == "POST":
        product.delete()
        return redirect("seller_dashboard:my_products")

    context = {"product": product}
    return render(request, "seller_dashboard/confirm_delete.html", context)


###############################################
@login_required
def my_orders_view(request):
    seller = request.user

    # جيب IDs بتاعة منتجات البائع الحالي
    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )

    order_items = []

    # لف على كل الطلبات الموجودة في Sale
    for sale in Sale.objects.select_related("order"):
        for item in sale.products:  # sale.products is JSON list
            product_id = item.get("id")
            if product_id in seller_product_ids:
                order_items.append(
                    {
                        "product": Product.objects.get(id=product_id),
                        "quantity": item.get("quantity", 1),
                        "price": item.get("price", 0),
                        "order": sale.order,
                    }
                )

    context = {"order_items": order_items}

    return render(request, "seller_dashboard/orders.html", context)


###############################################
@login_required
def sales_stats_view(request):
    seller = request.user

    # المنتجات الخاصة بالبائع
    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )

    # حدد تاريخ اليوم وابدأ تحسب 7 أيام ورا
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    # dict لجمع المبيعات لكل يوم
    sales_per_day = defaultdict(float)

    # هات الطلبات في آخر 7 أيام
    sales = Sale.objects.filter(
        date__date__range=(seven_days_ago, today)
    ).select_related("order")

    for sale in sales:
        for item in sale.products:
            product_id = item.get("id")
            if product_id in seller_product_ids:
                day = sale.date.date().strftime("%Y-%m-%d")
                quantity = item.get("quantity", 1)
                price = item.get("price", 0)
                sales_per_day[day] += quantity * price

    # حضر البيانات على شكل قائمة
    result = []
    for i in range(7):
        day = (seven_days_ago + timedelta(days=i)).strftime("%Y-%m-%d")
        result.append({"date": day, "sales": round(sales_per_day.get(day, 0), 2)})

    return JsonResponse(result, safe=False)


###############################################
