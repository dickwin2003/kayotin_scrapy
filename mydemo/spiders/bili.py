"""
bili - 哔哩哔哩的爬虫

BiliUtil.Util.av2bv(av)
该函数可将形如av170001，170001的av号转化为形如BV17x411w7KC的新编码方式

编码转换算法代码参考来源：https://blog.csdn.net/jkddf9h8xd9j646x798t/article/details/105124465

BiliUtil.Util.bv2av(bv)
该函数可将形如BV17x411w7KC的bv号转化为形如170001的旧编码方式

编码转换算法代码参考来源：https://blog.csdn.net/jkddf9h8xd9j646x798t/article/details/105124465

Author: hanayo
Date： 2023/12/11
"""

import scrapy
from scrapy import Selector, Request
from mydemo.items import BiliItem

alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
start_av = 102000
end_av = 103000


def bv_2_av(x):
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(x[v]) * 58 ** i
    return (r - 0x2_0840_07c0) ^ 0x0a93_b324


def av_2_bv(x):
    x = (x ^ 0x0a93_b324) + 0x2_0840_07c0
    r = list('BV1**4*1*7**')
    for v in [11, 10, 3, 8, 4, 6]:
        x, d = divmod(x, 58)
        r[v] = alphabet[d]
    return ''.join(r)


def fmt_info(src_info):
    """格式化一下获取到的文本信息，去掉换行和空格"""
    info = str(src_info).replace("\n", "").replace(" ", "")
    return info


class BiliSpider(scrapy.Spider):
    name = "bili_spider"
    allowed_domains = ['www.bilibili.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            # 如果有多条数据管道，需要在这里指定
            'mydemo.pipelines.BiliItemPipeline': 700,
        }
    }

    def start_requests(self):
        for av in range(start_av, end_av + 1):
            av_url = f"https://www.bilibili.com/video/av{av}/"
            yield Request(url=av_url)

    def parse(self, response, **kwargs):
        item = BiliItem()
        sel = Selector(response)
        item["bili_title"] = sel.css("h1.video-title").css('::text').get()
        if not item["bili_title"]:
            return False
        item["bili_author"] = fmt_info(sel.css("div.up-detail-top").css("a")[0].css('::text').get())

        item["bili_clicks"] = fmt_info(sel.css("div.video-info-detail-list").css("span.view.item::text").get())
        item["bili_comments"] = fmt_info(sel.css("div.video-info-detail-list").css("span.dm.item::text").get())
        item["bili_uptime"] = fmt_info(sel.css("div.video-info-detail-list").css("span.pubdate-text::text").get())

        item["bili_likes"] = sel.css("span.video-like-info.video-toolbar-item-text").css('::text').get()
        item["bili_favorites"] = sel.css("span.video-fav-info.video-toolbar-item-text").css('::text').get()
        item["bili_coins"] = sel.css("span.video-coin-info.video-toolbar-item-text").css('::text').get()
        item["bili_shares"] = sel.css("div.video-share-wrap.video-toolbar-left-item").css('::text').get()
        yield item


if __name__ == '__main__':
    print(av_2_bv(100023))
    print(bv_2_av("BV1AN41157h7"))
