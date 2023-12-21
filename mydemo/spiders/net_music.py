"""
net_music - 根据歌曲列表爬取评论


1.通过指定歌单链接，下载歌单列表，获取到歌曲id

---实际上该爬虫实现了第一步，先爬取歌曲信息。
2.通过歌曲id生成各歌曲url，依次进行请求
3.收集各个歌曲页面的评论，选取最热的前十

我的歌单：https://music.163.com/playlist?id=478849060
Author: hanayo
Date： 2023/12/14
"""

import scrapy
from scrapy import Request, Selector
import requests
from mydemo.static.my_cookie import net_cookie, user_agent
from mydemo.items import NetItem

play_list_id = "478849060"


class NetSpider(scrapy.Spider):
    name = "net_spider"
    allowed_domains = ["www.163.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'mydemo.pipelines.NetItemPipeline': 800,
        }
    }
    header = {
        'User-Agent': user_agent,
        'Cookie': net_cookie,
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/'
    }
    count = 0

    def start_requests(self):
        # 向指定歌单发出请求
        list_url = f"https://music.163.com/playlist?id={play_list_id}"
        yield Request(url=list_url, headers=self.header)

    def parse(self, response, **kwargs):
        # 匹配所有歌曲名的span
        sel = Selector(response)
        spans = sel.css("ul.f-hide")[0].css("a")

        for sp in spans:
            title = sp.css("::text").get()
            # print(title)
            url = sp.css("::attr(href)").get()
            # print(url)
            song_url = f"https://music.163.com{url}"
            # 注意，此处的dont_filter参数，如果不设置爬虫到这里就会自动结束了
            yield Request(url=song_url, headers=self.header, callback=self.parse_song, meta={'song_name': title},
                          dont_filter=True)

    def parse_song(self, response):
        song_sel = Selector(response)
        item = {
            "song_name": response.meta['song_name'],
            "singer_name": song_sel.css("p.des.s-fc4")[0].css("a::text").get(),
            "cd_name": song_sel.css("p.des.s-fc4")[1].css("a::text").get(),
            "song_url": response.url,
        }
        self.count += 1
        print(self.count)
        yield NetItem(item)


# if __name__ == '__main__':
#     song_url = "https://music.163.com/song?id=536624574"
#
#     res = requests.get(song_url, headers=header)
#     print(res.url)
#     sel = Selector(res)
#     print(sel.css("div.tit").css("::text").get())
#     print(sel.css("p.des.s-fc4")[0].css("a::text").get())
#     print(sel.css("p.des.s-fc4")[1].css("a::text").get())
#     # ミルク
#     print(sel.css("ul.f-hide")[0].css("a::attr(href)").get())
#     # /song?id=536624574


