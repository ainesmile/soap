from django.core.paginator import Paginator

def get_categoty(category):
        categories = {'normal': 'N', 'best': 'B', 'featured': 'F'}
        for item in categories:
            if item == category:
                return categories[category]
        raise KeyError('wrong category')

def get_breadcrumb_cn_name(category_name, brand_name):
    breadcrumb_category_names = {
        'best': '精选',
        'babycare': '母婴用品',
        'supplement': '营养保健',
        'skincare': '护肤用品',
        'bestfood': '畅销食品'
    }
    breadcrumb_brand_names = {
        'Pics': 'Pics',
        'Swisse': 'Swisse',
        'Ecostore': 'Ecostroe'
    }
    return (breadcrumb_category_names[category_name], breadcrumb_brand_names[brand_name])

def products_paginator(products, product_per_page):
    return Paginator(products, product_per_page)
