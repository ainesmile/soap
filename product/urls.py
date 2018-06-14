from django.urls import path
from .views import Products, Details

urlpatterns = [
    path('products/<str:category_name>/<str:subcategory>/', Products.as_view(), name='products'),
    path('<str:category>/<int:id>/', Details.as_view(), name='details'),
]