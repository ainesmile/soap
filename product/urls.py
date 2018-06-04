from django.urls import path
from .views import Details

urlpatterns = [
    path('<slug:category>/<int:id>/', Details.as_view(), name='details'),
]