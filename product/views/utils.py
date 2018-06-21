from django.core.paginator import Paginator
from product.models import Product

def get_product_list(filter_kwargs, products_per_page, page):
    product_filtered = Product.objects.filter(**filter_kwargs)
    paginator = Paginator(product_filtered, products_per_page)
    product_list = paginator.get_page(page)
    return product_list


def get_categoty(category_name):
        categories = {'normal': 'N', 'best': 'B', 'featured': 'F'}
        for item in categories:
            if item == category_name:
                return categories[category_name]
        raise KeyError('wrong category')

# def get_breadcrumb_cn_name(category_name, brand_name):
#     if category_name == 'best':
#         return [brand_name]
#     else:
#         breadcrumb_names = {
#             'babycare': '母婴用品',
#             'supplement': '营养保健',
#             'skincare': '护肤用品',
#             'bestfood': '畅销食品'
#         }
#         return [breadcrumb_names[category_name], brand_name]

