from django.views import View
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from product.models import Product

class Products(View):

    def get_categoty(self, category):
        categories = {'normal': 'N', 'best': 'B', 'featured': 'F'}
        for item in categories:
            if item == category:
                return categories[category]
        raise KeyError('wrong category')


    def get(self, request, category_name, subcategory):
        template_name = 'product/products.html'
        category = self.get_categoty(category_name)

        filter_kwargs = {"category": category, "subcategory": subcategory}
        product_list = Product.objects.filter(**filter_kwargs)
        
        return render(request, template_name, {"product_list": product_list,"categoty_name": category_name})


class Details(View):
    def get(self, request, category, id):
        template_name = 'product/details.html'
        context = {}
        return render(request, template_name, context)
        