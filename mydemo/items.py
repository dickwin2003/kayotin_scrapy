# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    score = scrapy.Field()
    motto = scrapy.Field()


class PixivItem(scrapy.Item):
    title = scrapy.Field()
    user_name = scrapy.Field()
    p_id = scrapy.Field()
    re_url = scrapy.Field()


class PixivDownloadItem(scrapy.Item):
    title = scrapy.Field()
    file_type = scrapy.Field()
    folder_name = scrapy.Field()
    is_many = scrapy.Field()
    headers = scrapy.Field()
    final_url = scrapy.Field()
