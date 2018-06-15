from django.views import View
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from product.models import Product
from product.views import utils

class Products(View):

    def get(self, request, category_name, subcategory):
        template_name = 'product/products.html'
        breadcrumb_cn_names = utils.get_breadcrumb_cn_name(category_name, subcategory)
        category = utils.get_categoty(category_name)
        filter_kwargs = {"category": category, "subcategory": subcategory}
        product_filter = Product.objects.filter(**filter_kwargs)

        product_per_page = 16
        paginator = utils.products_paginator(product_filter, product_per_page)
        page = request.GET.get('page')
        
        product_list = paginator.get_page(page)

        return render(request, template_name, {
            "product_list": product_list,
            "categoty_name": category_name,
            "breadcrumb_cn_names": breadcrumb_cn_names})


class Details(View):
    def get(self, request, category, id):
        template_name = 'product/details.html'
        context = {}
        return render(request, template_name, context)
        