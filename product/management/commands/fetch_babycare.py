import requests
import json
from lxml import html
import re
from time import sleep

from django.core.management.base import BaseCommand, CommandError




class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('save_option', nargs='?', type=str)
        parser.add_argument('source_file', nargs='?', type=str)
        parser.add_argument('saved_file', nargs='?', type=str)


    def handle(self, *args, **options):
        # source_data_file = 'data/source_babycare.json'
        # product_saved_file = 'data/babycare.json'

        save_option = options['save_option']
        source_file = options['source_file']
        saved_file = options['saved_file']

        with open(source_file, 'r') as source_data_file:
            source_data = json.loads(source_data_file.read())

        source_items = get_source_items(source_data)
        selectors = {
            'name_and_size': 'div[@class="gridProductStamp gridStamp"]/div[@class="gridProductStamp-product"]/div[@class="gridProductStamp-details"]/a/h3[@class="gridProductStamp-name"]/text()',
            'price_node': 'div[@class="gridProductStamp gridStamp"]/div[@class="gridProductStamp-product"]/div[@class="gridProductStamp-details"]/div[@class="gridProductStamp-priceContainer"]',
            'price_text': [
                'div[@class="gridProductStamp-price din-medium"]/text()',
                'span[@class="gridProductStamp-subPrice"]/text()',
                'a/span[@class="gridProductStamp-price club-text-colour din-medium"]/text()'
            ],
            'img': 'div[@class="gridProductStamp gridStamp"]/div[@class="gridProductStamp-product"]/a/img[@class="gridProductStamp-image"]/attribute::src'
        }


        all_products, all_img_request_urls, all_img_saved_dirs = get_all_data(source_items, selectors)
        print('fetched ', len(all_products), ' products and ', len(all_img_request_urls), ' img request urls and ', len(all_img_saved_dirs), 'img saved dirs.')
        assert len(all_products) == len(all_img_request_urls) == len(all_img_saved_dirs)
        if save_option == 'products':
            save_all_products(all_products, saved_file)
        elif save_option == 'imgs':
            save_all_imgs(all_img_request_urls, all_img_saved_dirs)
        elif save_option == 'all':
            save_all_products(all_products, saved_file)
            save_all_imgs(all_img_request_urls, all_img_saved_dirs)
        else:
            print('wrong save option.')

def save_all_products(all_products, product_saved_file):
    with open(product_saved_file, 'w') as file:
        file.write(json.dumps(all_products))
        print('saved ', len(all_products), ' products successfully.')

def save_all_imgs(all_img_request_urls, all_img_saved_dirs):
    for i in range(len(all_img_request_urls)):
        img_request_url = all_img_request_urls[i]
        img_data = requests.get(img_request_url).content
        img_saved_dir = all_img_saved_dirs[i]
        with open(img_saved_dir, 'wb') as img_file:
            img_file.write(img_data)
        print('saved img to', img_saved_dir)
    print('saved ', len(all_img_request_urls), 'successfully.')
        sleep(0.5)


def save_single_source_item_imgs(img_request_urls, img_saved_dirs):
    for i in range(len(img_request_urls)):
        img_request_url = img_request_urls[i]
        img_data = requests.get(img_request_url).content
        img_saved_dir = img_saved_dirs[i]
        with open(img_saved_dir, 'wb') as img_file:
            img_file.write(img_data)
        print('saved img to', img_saved_dir)
    print('saved ', len(img_request_urls), 'successfully.')
    sleep(0.5)


# Part for get data

def get_all_data(source_items, selectors):
    all_products = []
    all_img_request_urls = []
    all_img_saved_dirs = []
    for source_item in source_items:
        products, img_request_urls, img_saved_dirs = fetch_single_source_item_data(source_item, selectors)
        all_products.extend(products)
        all_img_request_urls.extend(img_request_urls)
        all_img_saved_dirs.extend(img_saved_dirs)
    return (all_products, all_img_request_urls, all_img_saved_dirs)


def get_source_items(source_data):
    # parser file 'data/source_babycare.json'
    source_items = []
    for source_item in source_data:
        base_url = source_item["base_url"]
        url_names = source_item["urls"]

        for category_4 in url_names:
            postfix_urls = url_names[category_4]
            for postfix_url in postfix_urls:
                url = base_url + postfix_url
                item = {
                    "category": source_item["category"],
                    "subcategory": source_item["subcategory"],
                    "category_3": source_item["category_3"],
                    "category_4": category_4,
                    "url": url,
                    "file_name": source_item["file_name"],
                    "img_saved_base_dir": source_item["img_saved_base_dir"]
                }
                source_items.append(item)

    return source_items


def fetch_single_source_item_data(source_item, selectors):
    base_url = source_item['url']

    first_tree = get_single_url_tree(base_url)

    trees = get_single_base_url_query_pages_trees(first_tree, base_url)

    categories = {
        "category": source_item["category"],
        "subcategory": source_item["subcategory"],
        "category_3": source_item["category_3"],
        "category_4": source_item["category_4"]
    }
    img_saved_base_dir = source_item["img_saved_base_dir"]
    products, img_request_urls, img_saved_dirs = parser_single_url_trees(trees, selectors, categories, img_saved_base_dir)
    return (products, img_request_urls, img_saved_dirs)


def parser_single_url_trees(trees, selectors, categories, img_saved_base_dir):
    products = []
    img_request_urls = []
    img_saved_dirs = []
    img_request_base_url = 'https://shop.countdown.co.nz'
    for tree in trees:
        names_with_size = get_single_tree_names_with_size(tree, selectors["name_and_size"])
        prices = get_single_tree_prices(tree, selectors["price_node"], selectors["price_text"])
        single_tree_img_request_urls, img_exts = get_single_tree_img_request_urls_and_exts(tree, selectors["img"], img_request_base_url)
        pic_names = get_single_tree_pic_names(names_with_size, img_exts)
        single_tree_products = get_single_tree_products(names_with_size, prices, pic_names, categories)
        single_tree_img_saved_dirs = get_single_tree_img_saved_dirs(img_saved_base_dir, pic_names)
        
        products.extend(single_tree_products)
        img_request_urls.extend(single_tree_img_request_urls)
        img_saved_dirs.extend(single_tree_img_saved_dirs)
    return (products, img_request_urls, img_saved_dirs)

def get_single_tree_products(names_with_size, prices, pic_names, categories):
    assert len(names_with_size) == len(prices) == len(pic_names)
    products = []
    for i in range(len(names_with_size)):
        name_with_size = names_with_size[i]
        name, size = get_name_and_size(name_with_size)
        price = prices[i]
        pic_name = pic_names[i]

        product = {
            "name": name,
            "fixed_price": price,
            "discounted_price": price,
            "size": size,
            "pic_name": pic_name
        }
        product.update(categories)
        products.append(product)
    return products

def get_single_tree_names_with_size(tree, name_and_size_selector):
    names_with_size = []
    name_size_content = tree.xpath(name_and_size_selector)
    for content in name_size_content:
        name_with_size = replace_slash_with_and(get_striped_content(content))
        names_with_size.append(name_with_size)
    return names_with_size

def get_single_tree_prices(tree, price_nodes_selector, price_text_selectors):
    prices = []
    price_nodes = tree.xpath(price_nodes_selector)
    for price_node in price_nodes:
        for price_text_selector in price_text_selectors:
            price_text_ele = price_node.xpath(price_text_selector)
            if price_text_ele:
                price_text = price_text_ele[0]
                price = get_price_number(price_text)
                prices.extend(price)
                break
    return prices

def get_single_tree_img_request_urls_and_exts(tree, img_selector, img_request_base_url):
    img_request_urls = []
    img_exts = []
    img_el_list = tree.xpath(img_selector)
    for img_name in img_el_list:
        img_request_urls.append(img_request_base_url + img_name)
        img_ext = get_img_ext(img_name)
        img_exts.append(img_ext)
    return (img_request_urls, img_exts)

def get_single_tree_pic_names(names_with_size, img_exts):
    assert len(names_with_size) == len(img_exts)
    pic_names = []
    for i in range(len(names_with_size)):
        pic_name = names_with_size[i].replace(' ', '-') + '.' + img_exts[i]
        pic_names.append(pic_name)
    return pic_names

def get_single_tree_img_saved_dirs(img_saved_base_dir, pic_names):
    img_saved_dirs = []
    for i in range(len(pic_names)):
        img_saved_dirs.append(img_saved_base_dir + pic_names[i])
    return img_saved_dirs

def replace_slash_with_and(content):
    return content.replace('/', ' and ')

def get_striped_content(content):
    for word in content.split('\n'):
        striped_content = word.strip()
        if striped_content:
            return striped_content

def get_name_and_size(name_with_size):
    words = name_with_size.split(' ')
    size = words.pop()
    name = ' '.join(words)
    return (name, size)

def get_price_number(price_text):
    striped_price_text = get_striped_content(price_text)
    price_number = re.findall(r"[\d+.]+", striped_price_text)
    return price_number

def get_img_ext(img_name):
    words = img_name.split('.')
    img_ext = words.pop()
    return img_ext


def get_single_base_url_query_pages_trees(first_tree, base_url):
    # get all page trees based on the same base_url
    trees = []
    query_page_urls = get_single_base_url_query_page_urls(first_tree, base_url)
    trees.append(first_tree)
    for query_page_url in query_page_urls[1:]:
        single_url_tree = get_single_url_tree(query_page_url)
        if single_url_tree is not None:
            trees.append(single_url_tree)
            print('fetched ', query_page_url)
    return trees

def get_single_url_tree(url):
    xpath_selector = '//div[@id="product-list"]'

    page = requests.get(url)
    tree_element = html.fromstring(page.content).xpath(xpath_selector)
    if tree_element:
        tree = tree_element[0]
        return tree

    # with open('data/baby-food-packer-meals.html', 'r') as f:
    #     tree = html.fromstring(f.read()).xpath(xpath_selector)[0]
    # return tree
    

    

def get_single_base_url_query_page_urls(tree, base_url):
    # get query urls based on the same base_url
    query_page_urls = []

    item_per_page = 24

    try:
        paging_ele = tree.xpath('//div[@class="paging-description hidden-tablet "]/text()')
        paging_text = paging_ele[0]
        paging = int(paging_text.split(' ')[0])
        page_number = int(paging / item_per_page) + 1
    except:
        page_number = 1

    for i in range(page_number):
        post_fix = '?page=' + str(i + 1)
        url = base_url + post_fix
        query_page_urls.append(url)
    return query_page_urls