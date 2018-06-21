from django.core.management.base import BaseCommand, CommandError
import json

from product.models import Product

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('data_file_name', nargs='?', type=str)

    def check_exist(self, product):
        kwargs = {
            "name": product["name"],
            "size": product["size"],
            "fixed_price": product["fixed_price"],
            "category": product["category"],
            "subcategory": product["subcategory"],
            "category_3": product["category_3"],
            "category_4": product["category_4"]
        }
        return Product.objects.filter(**kwargs)

    def handle(self, *args, **options):
        data_file_name = options['data_file_name']
        with open(data_file_name, 'r') as f:
            data = json.loads(f.read())
            
        save_product_number = 0
        exists_product_number = 0

        for product in data:
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
                    subcategory=product["subcategory"],
                    category_3=product["category_3"],
                    category_4=product["category_4"]
                )
                new_product.save()
                save_product_number += 1
                print(product["name"], 'with', product["size"], 'saved.')
        print('Successfully saved ', save_product_number, '. Already Exists ', exists_product_number)