from django.core.management.base import BaseCommand, CommandError

from product.models import Product
import json
import ast

class Command(BaseCommand):
    help = 'save products'

    def add_arguments(self, parser):
        parser.add_argument('file_names', nargs='?', type=str)

    def check_exist(self, product):
        kwargs = {
            "name": product["name"],
            "size": product["size"],
            "fixed_price": product["fixed_price"],
            "category": product["category"],
            "subcategory": product["subcategory"]
        }
        return Product.objects.filter(**kwargs)

    def handle(self, *args, **options):
        # file_names = ["data/best_pics.json", "data/best_swisse.json"]
        file_names_str = options['file_names']
        file_names = ast.literal_eval(file_names_str)

        save_product_number = 0
        exists_product_number = 0

        for file_name in file_names:
            with open(file_name, 'r') as f:
                products = json.loads(f.read())
                for product in products:
                    if self.check_exist(product):
                        exists_product_number += 1
                        print(product["name"], 'with', product["size"], 'already exists.')
                    else:
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
                        save_product_number += 1
                        print(product["name"], 'with', product["size"], 'saved.')
        
        print('Successfully saved ', save_product_number, '. Already Exists ', exists_product_number)
