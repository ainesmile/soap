from django.core.management.base import BaseCommand, CommandError

from product.models import Product
import json
import ast

class Command(BaseCommand):
    help = 'save products'

    def add_arguments(self, parser):
        parser.add_argument('file_names', nargs='?', type=str)

    def handle(self, *args, **options):
        file_names_str = options['file_names']
        file_names = ast.literal_eval(file_names_str)

        for file_name in file_names:
            with open(file_name, 'r') as f:
                products = json.loads(f.read())
                for product in products:
                    new_product = Product(
                        category=product["category"],
                        name=product["name"],
                        fixed_price=product["fixed_price"],
                        discounted_price=product["discounted_price"],
                        pic_name=product["pic_name"],
                        size=product["size"],
                        subcategory=product["subcategory"]
                    )
                    new_product.save()
        self.stdout.write('Successfully saved.')
