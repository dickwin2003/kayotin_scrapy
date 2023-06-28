import scrapy
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
import os
from mydemo.static.my_cookie import cookie, user_agent
from scrapy import Request


class PixivDownloadSpider(scrapy.Spider):
    name = "pixiv_download"
    allowed_domains = ["pixiv.net"]
    url_list = list()

    def start_requests(self):
        root_path = os.path.abspath(os.path.dirname(__file__))
        workbook = openpyxl.load_workbook(f"{root_path}/output/pixiv_weekly_rank数据.xlsx")  # type: Workbook
        worksheet = workbook["weekly"]  # type: Worksheet

        for row_num in range(2, worksheet.max_row + 1):
            url_obj = {
                "pic_name": f"{worksheet[f'A{row_num}']}_{worksheet[f'B{row_num}']}",
                "download_url": f"https://www.pixiv.net/ajax/illust/{worksheet[f'C{row_num}']}/pages?lang=zh",
                "referer": worksheet[f"D{row_num}"]
            }
            PixivDownloadSpider.url_list.append(url_obj)
        workbook.close()

        for url_obj in PixivDownloadSpider.url_list:
            header = {
                'User-Agent': user_agent,
                'Cookie': cookie,
                'referer': url_obj['referer']
            }
            yield Request(url=url_obj["download_url"], headers=header, callback=self.parse)

    def parse(self, response, **kwargs):
        datas = response.json()["body"]
        for data in datas:
            final_url = data["urls"]["original"]
            yield Request(url=final_url, headers={}, callback=self.parse_ajax)

    def parse_ajax(self, response):
        pass

