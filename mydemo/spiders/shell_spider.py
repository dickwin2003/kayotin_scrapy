"""
shell_spider - 贝壳网二手房放假信息爬虫

Author: kayotin
Date 2023/7/18
"""

import scrapy
from scrapy import Request, Selector
import re
import json
from mydemo.items import HouseItem
import datetime


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


def print_now():
    # 获取当前日期和时间
    now = datetime.datetime.now()

    # 格式化为字符串
    date_str = now.strftime('%Y-%m-%d')  # 格式化为年-月-日
    time_str = now.strftime('%H:%M:%S')  # 格式化为时:分:秒
    return f"{date_str} {time_str}"


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
    city_cn = city_dict[city_en]
    start_urls = [f"https://{city_en}.ke.com/ershoufang/"]
    rows_num = 0

    def parse(self, response, **kwargs):
        """从总的链接，获取到各行政区信息，然后，
        继续请求每个区的url，收到response后交给下一个parse处理，
        其中传递的参数有城市名，和区名。
        """
        selector = Selector(response)
        links_items = selector.css('a.CLICKDATA[data-action="source_type=PC小区列表筛选条件点击"]')
        print(f"获取了{self.city_cn}的{len(links_items)}个行政区信息-->{print_now()}")
        for item in links_items:
            city_en = ShellSpider.city_en
            url = f"https://{city_en}.ke.com{item.attrib['href']}"
            area_cn = item.xpath('string()').get()
            yield Request(url, callback=self.parse_street, meta={
                "city_en": city_en, "area_cn": area_cn,
                "city_cn": ShellSpider.city_dict[city_en],
            }, dont_filter=True)

    def parse_street(self, response):
        """
        从每个区的链接，获取到每个街道的链接，交给下一个parse处理，
        传递的参数，加上了街道名
        :param response:
        :return:
        """
        # bs_html = BeautifulSoup(response.text, "html.parser")
        # divs = bs_html.find_all("div", {"data-role": "ershoufang"})
        # items = divs[0].find_all("a", {"class": ""})
        # 更新成用Selector
        selector = Selector(response)
        divs = selector.css('div[data-role="ershoufang"]')
        items = divs[0].css('a:not([class])')

        meta = response.meta
        print(f"获取了{meta['area_cn']}的{len(items)}个街道信息--->{print_now()}")
        for item in items:
            meta["street_cn"] = item.xpath('string()').get()
            street_url = item.attrib['href']
            city_en = meta["city_en"]
            url = f"https://{city_en}.ke.com{street_url}"
            meta["street_url"] = url
            yield Request(url, callback=self.parse_house, meta=meta, dont_filter=True)

    def parse_house(self, response):
        # bs_html = BeautifulSoup(response.text, "html.parser")
        # pages = bs_html.find_all("div", {
        #     "class": "page-box house-lst-page-box",
        #     "comp-module": "page"
        # })
        # 改写成用Selector选择器
        selector = Selector(response)
        pages = selector.css('div.page-box.house-lst-page-box[comp-module="page"]')

        if len(pages):
            page_dict = json.loads(pages[0].attrib['page-data'])
            page_num = int(page_dict['totalPage'])
            # page_dict = json.loads(pages[0].get("page-data"))
        else:
            page_num = 0

        street_url = response.meta["street_url"]
        meta = response.meta
        if page_num:
            print(f"获取了{self.city_cn}的{meta['area_cn']}的{meta['street_cn']}街道的总页码是{page_num}-->{print_now()}")
            for num in range(1, page_num + 1):
                url = f"{street_url}pg{page_num}/"
                yield Request(url, callback=self.handle_info, meta=meta, dont_filter=True)

    def handle_info(self, response):
        # bs_html = BeautifulSoup(response.text, "html.parser")
        # info_divs = bs_html.find_all("div", {"class": "info clear"})
        info_divs = response.selector.css("div.info.clear")

        meta = response.meta
        for info_div in info_divs:
            community_name = fmt_info(info_div.css("div.positionInfo").xpath('string()').get())
            house_info = fmt_info(info_divs.css("div.houseInfo").xpath('string()').get())
            total_price = fmt_info(info_div.css("div.totalPrice.totalPrice2").xpath('string()').get())
            total_price = fmt_price(total_price)
            unit_price = fmt_info(info_div.css("div.unitPrice").xpath('string()').get())
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
            self.rows_num += 1
            if self.rows_num % 2000 == 0:
                print(f"已爬取{self.rows_num}条数据--->{print_now()}")

            yield HouseItem(item)
