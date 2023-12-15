"""
net_music - 根据歌曲列表爬取评论


1.通过指定歌单链接，下载歌单列表，获取到歌曲id
2.通过歌曲id生成各歌曲url，依次进行请求
3.收集各个歌曲页面的评论，选取最热的前十

我的歌单：https://music.163.com/#/my/m/music/playlist?id=478735988
Author: hanayo
Date： 2023/12/14
"""

import scrapy
from scrapy import Request, Selector
import requests
from http import cookiejar
import json
from mydemo.static.my_cookie import net_cookie, user_agent


class NetSpider(scrapy.Spider):
    name = "net_spider"
    allowed_domains = ["www.163.com"]
    url_list = list()
    custom_settings = {
        'ITEM_PIPELINES': {
            'mydemo.pipelines.NetPipeline': 800,
        }
    }

    def start_requests(self):
        pass
        # list_url = "https://music.163.com/#/my/m/music/playlist?id=478735988"
        # header = {
        #     'User-Agent': user_agent,
        #     'Cookie': net_cookie,
        # }
        # res = Request(url=list_url, headers=header)


if __name__ == '__main__':
    list_url = "https://music.163.com/#/my/m/music/playlist?id=478735988"
    header = {
        'User-Agent': user_agent,
        'Cookie': net_cookie,
    }
    res = Request(list_url, headers=header)
    print(res)
    # sel = Selector(res.)
    # print(sel.css("span.txt")[0].css("a::attr(href)").get())
    # print(sel.css("span.txt")[0].css("b::attr(title)").get())

