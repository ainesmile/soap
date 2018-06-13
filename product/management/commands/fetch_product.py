import requests
import json
from lxml import html
import re
from time import sleep

from django.core.management.base import BaseCommand, CommandError
import json

def get_names_and_sizes(tree):
    names = []
    sizes = []
    selector = 'div[@class="gridProductStamp gridStamp"]/div[@class="gridProductStamp-product"]/div[@class="gridProductStamp-details"]/a/h3[@class="gridProductStamp-name"]/text()'
    name_content = tree.xpath(selector)
    names_with_size = _get_striped_content(name_content)

    for name in names_with_size:
        name_split = name.split(' ')
        sizes.append(name_split.pop())
        names.append(' '.join(name_split))
    return (names, sizes, names_with_size)

def get_prices(tree):
    price_elements = _get_price_element(tree)
    striped_prices = _get_striped_content(price_elements)
    prices = _get_price_number(striped_prices)
    return prices

def get_img_names_with_size(names_with_size):
    img_names = []
    for name in names_with_size:
        img_name = "-".join(name.split(' ')) + '.jpg'
        img_names.append(img_name)
    return img_names

def get_products(names, sizes, prices, img_names_with_size, category, subcategory):
    products = []
    for i in range(len(names)):
        products.append({
            "name": names[i],
            "fixed_price": prices[i],
            "discounted_price": prices[i],
            "size": sizes[i],
            "pic_name": img_names_with_size[i],
            "category": category,
            "subcategory": subcategory
        })
    return products
        
def save_products_to_file(products, file_name):
    with open(file_name, 'w') as file:
        file.write(json.dumps(products))


def save_imgs(img_saved_base_dir, img_names, img_urls):
    for i in range(len(img_urls)):
        img_dir = img_saved_base_dir + img_names[i]
        _save_img(img_dir, img_urls[i])
        sleep(1)


def save_single_page_data(url, category, subcategory, products_save_file_name, img_saved_base_dir):

    page = requests.get(url)
    tree = html.fromstring(page.content).xpath('//div[@id="product-list"]')[0]

    # with open('pics.html', 'r') as f:
    #     tree = html.fromstring(f.read()).xpath('//div[@id="product-list"]')[0]

    names, sizes, names_with_size = get_names_and_sizes(tree)
    prices = get_prices(tree)
    img_names_with_size = get_img_names_with_size(names_with_size)
    img_urls = _get_img_urls(tree)
    _assert_fetch_data(names_with_size, sizes, prices, img_names_with_size, img_urls)


    products = get_products(names, sizes, prices, img_names_with_size, category, subcategory)
    save_products_to_file(products, products_save_file_name)

    save_imgs(img_saved_base_dir, img_names_with_size, img_urls)


def save_pages_data(source_data):
    for page_source in source_data:
        url = page_source["url"]
        category = page_source["category"]
        subcategory = page_source["subcategory"]
        file_name = page_source["file_name"]
        img_saved_base_dir = page_source["img_saved_base_dir"]
        
        save_single_page_data(url, category, subcategory, file_name, img_saved_base_dir)
        
def _get_striped_content(content):
    striped_content = []
    for c in content:
        for item in c.split('\n'):
            striped_item = item.strip()
            if striped_item:
                striped_content.append(striped_item)
    return striped_content

def _get_price_element(tree):
    price_elements = []
    selector = 'div[@class="gridProductStamp gridStamp"]/div[@class="gridProductStamp-product"]/div[@class="gridProductStamp-details"]/div[@class="gridProductStamp-priceContainer"]'
    price_nodes = tree.xpath(selector)
    selectors = [
        'div[@class="gridProductStamp-price din-medium"]/text()',
        'span[@class="gridProductStamp-subPrice"]/text()',
        'a/span[@class="gridProductStamp-price club-text-colour din-medium"]/text()'
    ]
    for price_node in price_nodes:
        for selector in selectors:
            price = price_node.xpath(selector)
            if price:
                price_elements.extend(price)
                break;
    return price_elements

def _get_price_number(prices):
    price_list = []
    for price in prices:
        price_list.extend((re.findall(r"[\d+.]+", price)))
    return price_list

def _get_img_urls(tree):
    img_urls = []
    base_url = 'https://shop.countdown.co.nz'
    selector = 'div[@class="gridProductStamp gridStamp"]/div[@class="gridProductStamp-product"]/a/img[@class="gridProductStamp-image"]/attribute::src'
    img_list = tree.xpath(selector)
    for img_name in img_list:
        img_urls.append(base_url + img_name)
    return img_urls

def _save_img(img_dir, img_url):
    img_data = requests.get(img_url).content
    # file_name = 'static/images/product/' + img_name
    with open(img_dir, 'wb') as handler:
        handler.write(img_data)


def _assert_fetch_data(names_with_size, sizes, prices, img_names_with_size, img_urls):
    assert len(names_with_size) == len(set(names_with_size))
    assert len(names_with_size) == len(sizes) == len(prices) == len(img_names_with_size) == len(img_urls)

    

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_data_file', nargs='?', type=str)
        
    def handle(self, *args, **options):
        source_data_file = options['source_data_file']

        with open(source_data_file, 'r') as source_file:
            source_data = json.loads(source_file.read())
        
        save_pages_data(source_data)

        self.stdout.write('Successfully saved.')

