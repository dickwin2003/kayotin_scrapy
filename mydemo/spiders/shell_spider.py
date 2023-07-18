"""
shell_spider - 贝壳网二手房放假信息爬虫

Author: kayotin
Date 2023/7/18
"""

import scrapy
from scrapy import Selector, Request
import re
from bs4 import BeautifulSoup
import json
from mydemo.items import HouseItem


def fmt_info(src_info):
    """格式化一下获取到的房子信息，去掉换行和空格"""
    info = str(src_info).replace("\n", "").replace(" ", "")
    return info


def fmt_price(price):
    """将带单位的数字，转换成浮点型数字"""
    # 首先去掉逗号
    string_num = re.sub(r',', '', price)

    # 使用正则表达式提取数字
    number = re.findall(r'\d+', string_num)[0]

    # 将提取的数字转换为float类型
    float_num = float(number)
    return float_num


class ShellSpider(scrapy.Spider):
    name = 'shell_spider'
    allowed_domains = ['www.ke.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            # 如果有多条数据管道，需要在这里指定
            'mydemo.pipelines.ShellItemPipeline': 200,
        }
    }
    city_en = "sh"
    city_dict = {
        "sh": "上海",
        "gz": "广州"
    }
    start_urls = ["https://sh.ke.com/ershoufang/"]

    def parse(self, response, **kwargs):
        """从总的链接，获取到各行政区信息，然后，
        继续请求每个区的url，收到response后交给下一个parse处理，
        其中传递的参数有城市名，和区名。
        """

        bs_html = BeautifulSoup(response.content, "html.parser")
        links_items = bs_html.find_all("a", {"class": "CLICKDATA",
                                             "data-action": "source_type=PC小区列表筛选条件点击"})
        for item in links_items:
            city_en = ShellSpider.city_en
            url = f"https://{city_en}.ke.com/{item.get('href')}"
            area_cn = item.text
            yield Request(url, callback=self.parse_street, meta={
                "city_en": city_en, "area_cn": area_cn,
                "city_cn": ShellSpider.city_dict[city_en],
            })

    def parse_street(self, response):
        """
        从每个区的链接，获取到每个街道的链接，交给下一个parse处理，
        传递的参数，加上了街道名
        :param response:
        :return:
        """
        bs_html = BeautifulSoup(response.content, "html.parser")
        divs = bs_html.find_all("div", {"data-role": "ershoufang"})
        items = divs[0].find_all("a", {"class": ""})

        meta = response.meta
        for item in items:
            meta["street_cn"] = item.text
            street_url = item.get('href')
            meta["street_url"] = street_url
            city_en = meta["city_en"]
            url = f"https://{city_en}.ke.com/{street_url}"
            yield Request(url, callback=self.parse_house, meta=meta)

    def parse_house(self, response):
        bs_html = BeautifulSoup(response.content, "html.parser")
        pages = bs_html.find_all("div", {
            "class": "page-box house-lst-page-box",
            "comp-module": "page"
        })
        if len(pages):
            page_dict = json.loads(pages[0].get("page-data"))
            page_num = int(page_dict["totalPage"])
        else:
            page_num = 0

        street_url = response.meta["street_url"]
        meta = response.meta

        if page_num:
            for num in range(1, page_num + 1):
                url = f"{street_url}pg{page_num}/"
                yield Request(url, callback=self.handle_info, meta=meta)

    house_city = scrapy.Field()
    house_area = scrapy.Field()
    house_street = scrapy.Field()
    house_community = scrapy.Field()
    house_info = scrapy.Field()
    house_total = scrapy.Field()
    house_unit = scrapy.Field()

    def handle_info(self, response):
        bs_html = BeautifulSoup(response.content, "html.parser")
        info_divs = bs_html.find_all("div", {"class": "info clear"})

        meta = response.meta
        for info_div in info_divs:
            community_name = fmt_info(info_div.find('div', class_='positionInfo').text)
            house_info = fmt_info(info_div.find('div', class_='houseInfo').text)
            total_price = fmt_info(info_div.find('div', class_='totalPrice totalPrice2').text)
            total_price = fmt_price(total_price)
            unit_price = fmt_info(info_div.find('div', class_='unitPrice').text)
            unit_price = fmt_price(unit_price)
            item = {
                "house_city": meta["city_cn"],
                "house_area": meta["area_cn"],
                "house_street": meta["street_cn"],
                "house_community": community_name,
                "house_info": house_info,
                "house_total": total_price,
                "house_unit": unit_price
            }
            yield HouseItem(item)
