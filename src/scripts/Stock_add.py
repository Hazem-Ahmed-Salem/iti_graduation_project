import os
import random
import ast

DATASET_DIR = os.path.join("static", "dataset")

def add_random_stock_to_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    try:
        products_data = {}
        exec(content, {}, products_data)
        products_list = products_data.get("products", [])
    except Exception as e:
        print(f" Error loading {filepath}: {e}")
        return

    modified = False
    for product in products_list:
        if "stock" not in product:
            product["stock"] = random.randint(5, 100)
            modified = True

    if modified:
        new_content = f"products = {products_list}"
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f" Updated stock in: {filepath}")
    else:
        print(f" Already has stock: {filepath}")

def main():
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith(".py"):
            file_path = os.path.join(DATASET_DIR, filename)
            add_random_stock_to_file(file_path)

if __name__ == "__main__":
    main()
