from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from orders.models import Order
from .forms import AddProductForm, EditProductForm
from django.contrib.auth.decorators import login_required
from user.utils import seller_required
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal

###############################################


@seller_required
def dashboard_view(request):
    seller = request.user

    
    total_products = Product.objects.filter(seller=seller).count()

    
    orders = Order.objects.filter(status='confirmed')

    total_orders = 0
    total_sales = 0

    
    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )

    seller_products = {p.id: p for p in Product.objects.filter(id__in=seller_product_ids)}

    
    for order in orders:
        order_has_product = False

        for item in order.products:
            product_id = item.get("product_id") or item.get("id")
            if product_id not in seller_product_ids:
                continue

            order_has_product = True

            quantity = int(item.get("quantity", 1))

            unit_price = item.get("price_per_unit")
            if unit_price is None:
                try:
                    unit_price = float(seller_products[product_id].price)
                except Exception:
                    unit_price = 0.0

            saved_line_total = item.get("order_price")
            if saved_line_total is not None:
                line_total = float(saved_line_total)
            else:
                line_total = float(unit_price) * quantity

            total_sales += line_total

        if order_has_product:
            total_orders += 1

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_sales": total_sales,
    }

    return render(request, "seller_dashboard/dashboard.html", context)

###############################################
@seller_required
def my_products_view(request):
    seller = request.user
    products = Product.objects.filter(seller=seller)

    context = {"products": products}

    return render(request, "seller_dashboard/my_products.html", context)

###############################################
@seller_required
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
@seller_required
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
@seller_required
def delete_product_view(request, pk):
    seller = request.user
    product = get_object_or_404(Product, pk=pk, seller=seller)

    if request.method == "POST":
        product.delete()
        return redirect("my_products")

    context = {"product": product}
    return render(request, "seller_dashboard/confirm_delete.html", context)

###############################################
@seller_required
def my_orders_view(request):
    seller = request.user

    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )

    seller_products = {
        p.id: p for p in Product.objects.filter(id__in=seller_product_ids)
    }

    order_items = []
    orders = Order.objects.all().order_by("-created_at")

    for order in orders:
        for item in order.products:
            product_id = item.get("product_id") or item.get("id")
            product = seller_products.get(product_id)
            if product is None:
                continue

            quantity = int(item.get("quantity", 1))


            unit_price = item.get("price_per_unit")
            if unit_price is None:
                try:
                    unit_price = float(product.price)
                except Exception:
                    unit_price = 0.0

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
@seller_required
@api_view(['GET'])
def sales_stats_view(request):
    seller = request.user

    seller_product_ids = set(
        Product.objects.filter(seller=seller).values_list("id", flat=True)
    )


    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)


    sales_per_day = defaultdict(float)


    seller_products = {p.id: p for p in Product.objects.filter(id__in=seller_product_ids)}

    orders = Order.objects.filter(
        created_at__date__range=(seven_days_ago, today),
        status='confirmed',
    )

    for order in orders:
        for item in order.products:
            product_id = item.get("product_id") or item.get("id")
            if product_id not in seller_product_ids:
                continue

            day = order.created_at.date().strftime("%Y-%m-%d")
            quantity = int(item.get("quantity", 1))

            unit_price = item.get("price_per_unit")
            if unit_price is None:
                try:
                    unit_price = float(seller_products[product_id].price)
                except Exception:
                    unit_price = 0.0

            saved_line_total = item.get("order_price")
            if saved_line_total is not None:
                line_total = float(saved_line_total)
            else:
                line_total = float(unit_price) * quantity

            sales_per_day[day] += line_total

  
    result = []
    for i in range(7):
        day = (seven_days_ago + timedelta(days=i)).strftime("%Y-%m-%d")
        result.append({"date": day, "sales": round(sales_per_day.get(day, 0), 2)})

    return Response({'success': result}, status=200)

###############################################
