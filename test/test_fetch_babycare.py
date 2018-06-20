import pytest
from lxml import html
import json
from product.management.commands import fetch_babycare


with open('data/data_test/source_babycare.json', 'r') as f:
    source_data = json.loads(f.read())
    
data = {
    'e_last_source_item': {'category': 'N', 'subcategory': 'Babycare', 'category_3': 'babytoiletries', 'category_4': 'baby-cream-lotion', 'url': 'https://shop.countdown.co.nz/shop/browse/baby-care/baby-toiletries/dermexa', 'file_name': 'data/babycare.json', 'img_saved_base_dir': 'media/normal/babycare/'},
    'e_source_item': {'category': 'N', 'subcategory': 'Babycare', 'category_3': 'babyfoods', 'category_4': 'other-baby-foods', 'url': 'https://shop.countdown.co.nz/shop/browse/baby-care/other-baby-foods', 'file_name': 'data/babycare.json', 'img_saved_base_dir': 'media/normal/babycare/'},
    'name_contents': ['\n                        Heinz Little Kids Cereal Bars Wholegrain Apple/blueberry 90g 15g bars 6pk\n                ', '\n                    Farex Baby Cereal Rice From 4 Months 125g\n                '],
    'e_striped_name_contents': ['Heinz Little Kids Cereal Bars Wholegrain Apple/blueberry 90g 15g bars 6pk', 'Farex Baby Cereal Rice From 4 Months 125g'],
    "names_with_size": ['Heinz Little Kids Cereal Bars Wholegrain Apple and blueberry 90g 15g bars 6pk', 'Farex Baby Cereal Rice From 4 Months 125g'],
    "names": ['Heinz Little Kids Cereal Bars Wholegrain Apple and blueberry 90g 15g bars', 'Farex Baby Cereal Rice From 4 Months'],
    "sizes": ['6pk', '125g'],
    "prices": ['3.59', '3.59'],
    "img_request_urls": ['https://shop.countdown.co.nz/Content/ProductImages/big/9300657160388.jpg/Farex-Baby-Cereal-Original-Multigrain-6-Mth-.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9300657160364.jpg/Farex-Baby-Cereal-Rice-From-4-Months.jpg'],
    "pic_names": ['Heinz-Little-Kids-Cereal-Bars-Wholegrain-Apple-and-blueberry-90g-15g-bars-6pk.jpg', 'Farex-Baby-Cereal-Rice-From-4-Months-125g.jpg'],
    "categories": {
        "category": "N",
        "subcategory": "Babycare",
        "category_3": "babyfoods",
        "category_4": "other-baby-foods"
    },
    "products": [
        {'name': 'Heinz Little Kids Cereal Bars Wholegrain Apple and blueberry 90g 15g bars', 'fixed_price': '3.59', 'discounted_price': '3.59', 'size': '6pk', 'pic_name': 'Heinz-Little-Kids-Cereal-Bars-Wholegrain-Apple-and-blueberry-90g-15g-bars-6pk.jpg', 'category': 'N', 'subcategory': 'Babycare', 'category_3': 'babyfoods', 'category_4': 'other-baby-foods'},
        {'name': 'Farex Baby Cereal Rice From 4 Months', 'fixed_price': '3.59', 'discounted_price': '3.59', 'size': '125g', 'pic_name': 'Farex-Baby-Cereal-Rice-From-4-Months-125g.jpg', 'category': 'N', 'subcategory': 'Babycare', 'category_3': 'babyfoods', 'category_4': 'other-baby-foods'}
    ],
    "img_saved_dirs": ['media/normal/babycare/Heinz-Little-Kids-Cereal-Bars-Wholegrain-Apple-and-blueberry-90g-15g-bars-6pk.jpg', 'media/normal/babycare/Farex-Baby-Cereal-Rice-From-4-Months-125g.jpg']
}

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

with open('data/baby-food-packer-meals.html', 'r') as f:
    tree = html.fromstring(f.read()).xpath('//div[@id="product-list"]')[0]


def test_get_source_items():
    source_items = fetch_babycare.get_source_items(source_data)
    
    assert len(source_items) == 7
    last_source_item = source_items[6]
    assert last_source_item == data["e_last_source_item"]

def test_get_single_url_tree():
    single_url_tree = fetch_babycare.get_single_url_tree('fakeurl')
    assert single_url_tree.attrib == {'id': 'product-list'}

def test_get_single_base_url_query_pages_trees():
    base_url = 'fakeurl'
    first_tree = fetch_babycare.get_single_url_tree('fakeurl')
    trees = fetch_babycare.get_single_base_url_query_pages_trees(first_tree, base_url)

    assert len(trees) == 2


def test_get_single_base_url_query_page_urls():
    query_page_urls = fetch_babycare.get_single_base_url_query_page_urls(tree, 'fakeurl')
    assert len(query_page_urls) == 2
    assert query_page_urls == ['fakeurl?page=1', 'fakeurl?page=2']

def test_get_striped_content():
    striped_name_content = fetch_babycare.get_striped_content(data["name_contents"][0])
    assert striped_name_content == data["e_striped_name_contents"][0]

def test_replace_slash_with_and():
    new_content = fetch_babycare.replace_slash_with_and('apple/banana')
    assert new_content == 'apple and banana'

def test_get_name_and_size():
    name, size = fetch_babycare.get_name_and_size(data["names_with_size"][0])
    assert name == data["names"][0]
    assert size == data["sizes"][0]

def test_get_price_number():
    price_content = '\n      was $3.59      \n'
    price_number = fetch_babycare.get_price_number(price_content)
    assert price_number == ['3.59']

def test_get_img_ext():
    img_name = '/Content/ProductImages/big/9300657160388.jpg/Farex-Baby-Cereal-Original-Multigrain-6-Mth-.jpg'
    postfix = fetch_babycare.get_img_ext(img_name)
    assert postfix == 'jpg'

def test_get_single_tree_prices():
    prices = fetch_babycare.get_single_tree_prices(tree, selectors["price_node"], selectors["price_text"])
    assert prices == data["prices"]

def test_get_single_tree_img_request_urls_and_exts():
    urls, exts = fetch_babycare.get_single_tree_img_request_urls_and_exts(tree, selectors["img"], 'https://shop.countdown.co.nz')
    assert urls == data["img_request_urls"]
    assert exts[0] == 'jpg'

def test_get_single_tree_names_with_size():
    names_with_size = fetch_babycare.get_single_tree_names_with_size(tree, selectors["name_and_size"])
    assert names_with_size == data["names_with_size"]

def test_get_single_tree_pic_names():
    _, exts = fetch_babycare.get_single_tree_img_request_urls_and_exts(tree, selectors["img"], 'https://shop.countdown.co.nz')
    pic_names = fetch_babycare.get_single_tree_pic_names(data["names_with_size"], exts)
    assert pic_names == data["pic_names"]

def test_get_single_tree_products():
    products = fetch_babycare.get_single_tree_products(data["names_with_size"], data["prices"], data["pic_names"], data["categories"])
    assert products == data["products"]

def test_get_single_tree_img_saved_dirs():
    img_saved_base_dir = "media/normal/babycare/"
    img_saved_dirs = fetch_babycare.get_single_tree_img_saved_dirs(img_saved_base_dir, data["pic_names"])
    assert img_saved_dirs == data["img_saved_dirs"]


def test_fetch_single_source_item_data():
    products, img_request_urls, img_saved_dirs = fetch_babycare.fetch_single_source_item_data(data["e_source_item"], selectors)
    assert products == data["products"]*2
    assert img_request_urls == data["img_request_urls"]*2
    assert img_saved_dirs == data["img_saved_dirs"]*2

def test_get_all_data():
    all_products, all_img_request_urls, all_img_saved_dirs = fetch_babycare.get_all_data([data["e_source_item"]], selectors)
    assert all_products == data["products"]*2
    assert all_img_request_urls == data["img_request_urls"]*2
    assert all_img_saved_dirs == data["img_saved_dirs"]*2