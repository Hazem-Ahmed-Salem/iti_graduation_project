from products.models import Product,Category
from products.products_list import products 
from django.core.files.base import ContentFile
import urllib.request
from io import BytesIO

def import_products():
    for item in products:
        # إنشاء أو جلب التصنيف
        category, _ = Category.objects.get_or_create(name=item['category'])

        # تحميل الصورة من الإنترنت إلى BytesIO
        response = urllib.request.urlopen(item['thumbnail'])
        img_data = response.read()
        img_file = ContentFile(img_data)

        # إنشاء المنتج
        product = Product.objects.create(
            name=item['title'],
            description=item['description'],
            price=item['price'],
            category=category,
            stock=item['stock'],
        )

        # حفظ الصورة في المنتج
        product.image.save(f"{item['title'].replace(' ', '_')}.webp", img_file)
        product.save()

    print("✅ Products imported successfully!")