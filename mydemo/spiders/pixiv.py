import scrapy
from scrapy import Request


class PixivSpider(scrapy.Spider):
    name = "pixiv"
    allowed_domains = ["www.pixiv.net"]
    custom_settings = {
        'ITEM_PIPELINES': {
            # 如果有多条数据管道，需要在这里指定
            'mydemo.pipelines.PixivPipeline': 400,
        }
    }

    def start_requests(self):
        for page in range(1, 6):
            yield Request(url=f"https://www.pixiv.net/ranking.php?mode=weekly&p={page}&format=json")

    def parse(self, response, **kwargs):
        """parse 方法是 Scrapy 框架中默认调用的方法，它会在 Spider 启动后自动调用，用于处理抓取的网页数据。
        在 parse 方法中，您可以编写代码来提取网页中的数据，并将其存储到数据仓库或者输出到文件中。"""
        datas = response.json()["contents"]
        for data in datas:
            yield {
                "title": data["title"],
                "user_name": data["user_name"],
                "p_id": data["illust_id"],
                "re_url": f"https://www.pixiv.net/artworks/{data['illust_id']}"
            }




