from django.views import View
from django.views.generic.base import TemplateView
from django.shortcuts import render 
from django.http import HttpResponse
from product.models import Product

class Home(View):
    def get(self, requset):
        featured = Product.objects.filter(category='F')
        return render(requset, 'core/home.html', {"featured": featured})