from django.views import View
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from product.models import Product
from product.views import utils



class Best(View):
    def get(self, request, category_name, category_3):
        template_name = 'product/products.html'

        category = utils.get_categoty(category_name)
        category_3 = category_3.lower()

        filter_kwargs = {"category": category, "category_3": category_3}
        products_per_page = 16
        page = request.GET.get('page')
        product_list = utils.get_product_list(filter_kwargs, products_per_page, page)

        return render(request, template_name, {
            "product_list": product_list,
            "categoty_name": category_name,
            "breadcrumb_cn_names": [category_3]})



class Details(View):
    def get(self, request, category, id):
        template_name = 'product/details.html'
        context = {}
        return render(request, template_name, context)
        