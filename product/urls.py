from django.urls import path
from product.views import pages

urlpatterns = [
    path('products/<str:category_name>/<str:subcategory>/', pages.Products.as_view(), name='products'),
    path('<str:category>/<int:id>/', pages.Details.as_view(), name='details'),
]