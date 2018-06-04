from django.views import View
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
# from product.models import Product

class Details(View):

    

    def get(self, request, category, id):
        template_name = 'product/details.html'
        context = {}
        return render(request, template_name, context)
        