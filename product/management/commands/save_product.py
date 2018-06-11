from django.core.management.base import BaseCommand, CommandError

from product.models import Product
import json

class Command(BaseCommand):
    help = 'save products'

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='?', type=str)
        parser.add_argument('category', nargs='?', type=str)

    def handle(self, *args, **options):
        file_name = options['file_name']
        category = options['category']


        try:
            with open(file_name, 'r') as f:
                products = json.loads(f.read())
                
                for subcategory, product_list in products.items():
                    for product_item in product_list:
                        new_product = Product(
                            category=category,
                            name=product_item["name"],
                            fixed_price = product_item["fixed_price"],
                            discounted_price = product_item["discounted_price"],
                            pic_name = product_item["pic_name"],
                            size = product_item["size"],
                            subcategory = subcategory)
                        new_product.save()
        except:
            raise CommandError("save product failed")

        self.stdout.write('Successfully saved.')
