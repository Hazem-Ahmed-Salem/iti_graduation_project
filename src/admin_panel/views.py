# # admin_panel/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Customer
# from .forms import CustomerForm 
# from products.models import Product,Category
# from django.http import HttpResponse
# from django.shortcuts import render
# import os
# import importlib.util
# from django.conf import settings
# from django.core.paginator import Paginator

# from .models import order
# # from django.contrib.auth.decorators import login_required, user_passes_test

# # def is_admin(user):
# #     return user.is_superuser 
# # @login_required
# # @user_passes_test(is_admin)
# customers = Customer.objects.all()

# def customers_view(request):
    
#     return render(request, 'admin_panel/customers.html',{'customers': customers})

# def delete_customer(request, customer_id):
#     customer_obj = get_object_or_404(customers, id=customer_id)
#     customer_obj.delete()
#     return redirect('customers')



# def add_customer(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#     else:
#         form = CustomerForm()

#     return render(request, 'admin_panel/add_customer.html', {'form': form})

# def products_view(request):
#     category_id = request.GET.get('category')
#     if category_id:
#         products = Product.objects.filter(category_id=category_id)
#     else:
#         products = Product.objects.all()

#     categories = Category.objects.all()
#     return render(request, 'admin_panel/products.html', {
#         'products': products,
#         'categories': categories,
#         'selected_category': int(category_id) if category_id else None,
#     })
#     return render(request,'admin_panel/products.html')




# def Dashboard(request):
#     return render(request,"admin_panel_templates/dashboard.html")


# def display_Electronic_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Electronic products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})


# def display_Kitchen_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Kitchen products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})





# def display_Beauty_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Beauty products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})




# def display_Makeup_products(request):
#     file_path = os.path.join(settings.STATIC_ROOT, 'dataset/Makeup products.py')
    
#     spec = importlib.util.spec_from_file_location("products_module", file_path)
#     products_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(products_module)
    
#     products = products_module.products
    
#     return render(request, 'admin_panel_templates/products.html', {'products': products})





# def Orders(request):
#     Orders=order.objects.all()

#     paginator = Paginator(Orders,4) 
#     page_number = request.GET.get('page')
#     OrdersList = paginator.get_page(page_number)

    
#     return render(request,"admin_panel_templates/orders.html",{"OrdersList":OrdersList})



# def Recommendation(request):
#     return render(request,"admin_panel_templates/recommendation.html")




# def Cancelled(request):
#     OrdersList=order.objects.all()


#     return render(request,"admin_panel_templates/cancelled.html",{"OrdersList":OrdersList})


# def Done(request):
#     Orders=order.objects.all()
#     paginator = Paginator(Orders,4) 
#     page_number = request.GET.get('page')
#     OrdersList = paginator.get_page(page_number)


#     return render(request,"admin_panel_templates/done orders.html",{"OrdersList":OrdersList})

