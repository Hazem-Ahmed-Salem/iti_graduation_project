import re
import random
import importlib.util
import os
import sys
import django


project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from products.models import Product, Category, Stock
from django.contrib.auth import get_user_model

User = get_user_model()

DATASET_DIR = os.path.join(project_path,"static", "dataset")
print(DATASET_DIR)

def parse_price(price_str):
    if not price_str:
        return 0.0
    numbers = re.findall(r"\d+[\.\d+]?", price_str.replace(",", ""))
    return float(numbers[0]) if numbers else 0.0


def load_products_from_file(filepath):
    spec = importlib.util.spec_from_file_location("module.name", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.products

default_seller = User.objects.filter(user_role='seller').first()
if not default_seller:
    print(" No seller with user_role='seller' found.")
    sys.exit()

for filename in os.listdir(DATASET_DIR):
    if not filename.endswith(".py"):
        continue

    category_name = filename.replace("_", " ").replace(".py", "").title()
    filepath = os.path.join(DATASET_DIR, filename)
    products_list = load_products_from_file(filepath)

    category, _ = Category.objects.get_or_create(name=category_name)

    for product_data in products_list:
        product_name = product_data.get("name")
        price = parse_price(product_data.get("actual_price"))
        image_url = product_data.get("image")
        stock_quantity = product_data.get("stock", random.randint(10, 100))

        if not Product.objects.filter(name=product_name).exists():

            product = Product.objects.create(
                seller=default_seller,
                name=product_name,
                category=category,
                price=price,
                URL_image=image_url,
                image=None,
                is_featured=True,
            )


            Stock.objects.create(product=product, quantity=stock_quantity)

            print(f"Added: {product_name} (stock: {stock_quantity})")
        else:
            print(f"Skipped (already exists): {product_name}")
