import pytest
from lxml import html
from product.management.commands import fetch_product


with open('data/pics.html', 'r') as f:
    tree = html.fromstring(f.read()).xpath('//div[@id="product-list"]')[0]

data = {
    "price_content": ['$6.50\xa0ea', '$6.50\xa0ea', '$6.50\xa0ea', '$5.99\xa0ea', '$15.99\xa0ea', '$10.99\xa0ea', '$10.99\xa0ea', '$8.99\xa0ea', 'was $7.99'],
    "e_price_element": ['\n                            $6.50\xa0ea\n                    ', '\n                            $6.50\xa0ea\n                    ', '\n                            $6.50\xa0ea\n                    ', '\n                            $5.99\xa0ea\n                    ', '$15.99\xa0ea', '\n                            $10.99\xa0ea\n                    ', '\n                            $10.99\xa0ea\n                    ', '\n                            $8.99\xa0ea\n                    ', '\n                            was $7.99\n                        '],
    "e_names_without_size": ['Pics Peanut Butter Smooth', 'Pics Peanut Butter Crunchy No Salt jar', 'Pics Peanut Butter Crunchy', 'Pics Peanut Butter Slugs 180g', 'Pics Peanut Butter Crunchy', 'Pics Spread Almond Butter', 'Pics Spread Cashew Butter', 'Lewis Rd Creamery Ice Cream Pics Peanut Butter', 'Pics Really Good Peanut Oil'],
    "e_size": ['380g', '380g', '380g', '6pk', '1kg', '195g', '195g', '470ml', '250ml'],
    "e_names": ['Pics Peanut Butter Smooth 380g', 'Pics Peanut Butter Crunchy No Salt jar 380g', 'Pics Peanut Butter Crunchy 380g', 'Pics Peanut Butter Slugs 180g 6pk', 'Pics Peanut Butter Crunchy 1kg', 'Pics Spread Almond Butter 195g', 'Pics Spread Cashew Butter 195g', 'Lewis Rd Creamery Ice Cream Pics Peanut Butter 470ml', 'Pics Really Good Peanut Oil 250ml'],
    "e_prices": ['6.50', '6.50', '6.50', '5.99', '15.99', '10.99', '10.99', '8.99', '7.99'],    
    "e_img_names": ['Pics-Peanut-Butter-Smooth-380g.jpg', 'Pics-Peanut-Butter-Crunchy-No-Salt-jar-380g.jpg', 'Pics-Peanut-Butter-Crunchy-380g.jpg', 'Pics-Peanut-Butter-Slugs-180g-6pk.jpg', 'Pics-Peanut-Butter-Crunchy-1kg.jpg', 'Pics-Spread-Almond-Butter-195g.jpg', 'Pics-Spread-Cashew-Butter-195g.jpg', 'Lewis-Rd-Creamery-Ice-Cream-Pics-Peanut-Butter-470ml.jpg', 'Pics-Really-Good-Peanut-Oil-250ml.jpg'],
    "name_content": ['\n                    Pics Peanut Butter Smooth 380g\n                ', '\n                    Pics Peanut Butter Crunchy No Salt jar 380g\n                ', '\n                    Pics Peanut Butter Crunchy 380g\n                ', '\n                    Pics Peanut Butter Slugs 180g 6pk\n                ', '\n                    Pics Peanut Butter Crunchy 1kg\n                ', '\n                    Pics Spread Almond Butter 195g\n                ', '\n                    Pics Spread Cashew Butter 195g\n                ', '\n                    Lewis Rd Creamery Ice Cream Pics Peanut Butter 470ml\n                ', '\n                    Pics Really Good Peanut Oil 250ml\n                '],
    "e_img_urls": ['https://shop.countdown.co.nz/Content/ProductImages/big/9421901881160.jpg/Pics-Peanut-Butter-Smooth.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881061.jpg/Pics-Peanut-Butter-Crunchy-No-Salt.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881009.jpg/Pics-Peanut-Butter-Crunchy.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881641.jpg/Pics-Peanut-Butter-Slugs-180g.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881054.jpg/Pics-Peanut-Butter-Crunchy.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881511.jpg/Pics-Spread-Almond-Butter.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881535.jpg/Pics-Spread-Cashew-Butter.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421903483744.jpg/Lewis-Rd-Creamery-Ice-Cream-Pics-Peanut-Butter.jpg', 'https://shop.countdown.co.nz/Content/ProductImages/big/9421901881450.jpg/Pics-Really-Good-Peanut-Oil.jpg']
}


def test_get_names_and_sizes():
    assert fetch_product.get_names_and_sizes(tree) == (data["e_names_without_size"], data["e_size"], data["e_names"])

def test_get_prices():
    assert fetch_product.get_prices(tree) == data["e_prices"]

def test_get_img_names_with_size():
    assert fetch_product.get_img_names_with_size(data["e_names"]) == data["e_img_names"]

def test_get_products():
    products = fetch_product.get_products(data["e_names_without_size"], data["e_size"], data["e_prices"], data["e_img_names"], 'B', 'Pics')
    product = products[0]
    name = product["name"]
    category = product["category"]
    subcategoty = product["subcategory"]
    assert (name == data["e_names_without_size"][0]) and (category == 'B') and (subcategoty == 'Pics')

def test_get_striped_content():
    assert fetch_product._get_striped_content(data["name_content"]) == data["e_names"]

def test_get_price_elememt():
    assert fetch_product._get_price_element(tree) == data["e_price_element"]

def test_get_price_number():
    assert fetch_product._get_price_number(data["price_content"]) == data["e_prices"]

def test_get_img_urls():
    assert fetch_product._get_img_urls(tree) == data["e_img_urls"]


def test_cal_page_urls():
    assert fetch_product._cal_page_urls(tree, 'first_page_url') == ['first_page_url&page=1']


