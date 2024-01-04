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
    folder_name = scrapy.Field()
    is_many = scrapy.Field()
    headers = scrapy.Field()
    final_urls = scrapy.Field()


class HouseItem(scrapy.Item):
    house_city = scrapy.Field()
    house_area = scrapy.Field()
    house_street = scrapy.Field()
    house_community = scrapy.Field()
    house_info = scrapy.Field()
    house_total = scrapy.Field()
    house_unit = scrapy.Field()


class BiliItem(scrapy.Item):
    bili_title = scrapy.Field()
    bili_author = scrapy.Field()
    bili_clicks = scrapy.Field()
    bili_comments = scrapy.Field()
    bili_uptime = scrapy.Field()
    bili_likes = scrapy.Field()
    bili_favorites = scrapy.Field()
    bili_coins = scrapy.Field()
    bili_shares = scrapy.Field()


class NetItem(scrapy.Item):
    song_name = scrapy.Field()
    singer_name = scrapy.Field()
    cd_name = scrapy.Field()
    song_url = scrapy.Field()


class NetWordItem(scrapy.Item):
    song_name = scrapy.Field()
    user_name = scrapy.Field()
    content = scrapy.Field()
    comment_date = scrapy.Field()
    liked_count = scrapy.Field()
