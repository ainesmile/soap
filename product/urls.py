from django.urls import path
from product.views import pages

urlpatterns = [
    path('products/<str:category_name>/<str:category_3>/', pages.Best.as_view(), name='best'),
    path('<str:category>/<int:id>/', pages.Details.as_view(), name='details'),
]