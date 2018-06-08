from django.core.management.base import BaseCommand, CommandError

from product.models import Featured
import json

class Command(BaseCommand):
    help = 'save featured products'

    def handle(self, *args, **options):
        with open('data/featured.json', 'r') as f:
            products = json.loads(f.read())
            for category, product_list in products.items():
                for product in product_list:
                    new_featured = Featured(
                        name=product["name"],
                        fixed_price = product["fixed_price"],
                        discounted_price = product["discounted_price"],
                        pic_name = product["pic_name"],
                        size = product["size"],
                        category = category)
                    new_featured.save()
