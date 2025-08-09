from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from orders.models import Order
from orders.models import Sale  
from .forms import AddProductForm, EditProductForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal

###############################################


@login_required
@never_cache
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
@never_cache
def my_products_view(request):
    seller = request.user
    products = Product.objects.filter(seller=seller)

    context = {"products": products}

    return render(request, "seller_dashboard/my_products.html", context)

###############################################
@login_required
@never_cache
def add_product_view(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(seller=request.user)
            return redirect("my_products")
    else:
        form = AddProductForm()

    context = {"form": form}
    return render(request, "seller_dashboard/add_product.html", context)

###############################################
@login_required
@never_cache
def edit_product_view(request, pk):
    seller = request.user
    product = get_object_or_404(Product, pk=pk, seller=seller)

    if request.method == "POST":
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("my_products")
    else:
        form = EditProductForm(instance=product)

    context = {"form": form, "product": product}
    return render(request, "seller_dashboard/edit_product.html", context)

###############################################
@login_required
@never_cache
def delete_product_view(request, pk):
    seller = request.user
    product = get_object_or_404(Product, pk=pk, seller=seller)

    if request.method == "POST":
        product.delete()
        return redirect("my_products")

    context = {"product": product}
    return render(request, "seller_dashboard/confirm_delete.html", context)

###############################################
@login_required
@never_cache
def my_orders_view(request):
    seller = request.user

    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )

    # Preload seller products to avoid N+1 queries
    seller_products = {
        p.id: p for p in Product.objects.filter(id__in=seller_product_ids)
    }

    order_items = []
    orders = Order.objects.all().order_by("-created_at")

    for order in orders:
        for item in order.products:
            # Support both legacy key names ("id") and current ("product_id")
            product_id = item.get("product_id") or item.get("id")
            product = seller_products.get(product_id)
            if product is None:
                continue

            quantity = int(item.get("quantity", 1))

            # Prefer saved price at checkout time; fall back to current product price
            unit_price = item.get("price_per_unit")
            if unit_price is None:
                try:
                    unit_price = float(product.price)
                except Exception:
                    unit_price = 0.0

            # Prefer saved line total if present for accuracy
            saved_line_total = item.get("order_price")
            if saved_line_total is not None:
                total_price = float(saved_line_total)
            else:
                total_price = float(unit_price) * quantity

            order_items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "price": unit_price,
                    "total_price": total_price,
                    "date": order.created_at,
                    "order_id": order.id,
                }
            )

    context = {"order_items": order_items}

    return render(request, "seller_dashboard/orders.html", context)

###############################################
@login_required
@never_cache
@api_view(['GET'])
def sales_stats_view(request):
    seller = request.user

    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )


    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)


    sales_per_day = defaultdict(float)


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

  
    result = []
    for i in range(7):
        day = (seven_days_ago + timedelta(days=i)).strftime("%Y-%m-%d")
        result.append({"date": day, "sales": round(sales_per_day.get(day, 0), 2)})

    return Response({'success': result}, status=200)

###############################################
