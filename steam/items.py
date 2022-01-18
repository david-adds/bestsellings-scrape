# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from scrapy.selector import Selector
from itemloaders.processors import TakeFirst, MapCompose

def remove_html(review_summary):
    cleaned_review_summary = ''
    try:
        cleaned_review_summary = remove_tags(review_summary)
    except TypeError:
        cleaned_review_summary = 'No reviews'

    return cleaned_review_summary


def get_platforms(one_class):
    platforms = []
    platform = one_class.split(' ')[-1]
    if platform=='win':
        platforms.append('Windows')
    elif platform=='mac':
        platforms.append('Mac OS')
    elif platform=='linux':
        platforms.append('Linux')
    else:
        platforms.append('VR Supported')
        
    return platforms


def get_original_price(html_markup):
    original_price = ''
    selector_obj = Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(".//div[contains(@class,'search_price discounted')]")
    if len(div_with_discount) > 0:
        original_price = div_with_discount.xpath(".//span/strike/text()").get()
    else:
        original_price = selector_obj.xpath("normalize-space(.//div[contains(@class,'search_price')]/text())").get()      
    return original_price


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor = TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor = TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor = MapCompose(get_platforms)
    )
    reviews_summary = scrapy.Field(
        input_processor = MapCompose(remove_html),
        output_processor = TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor = MapCompose(get_original_price),
        output_processor = TakeFirst()
    )
    discounted_price = scrapy.Field()
    discount_rate = scrapy.Field()
