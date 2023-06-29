"""爬虫并下载"""

import scrapy
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
import os
from mydemo.static.my_cookie import cookie, user_agent
from scrapy import Request
from mydemo.items import PixivDownloadItem


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
            yield Request(url=url_obj["download_url"],
                          headers=header,
                          callback=self.parse,
                          meta={"headers": header, "pic_name": url_obj["pic_name"]})

    def parse(self, response, **kwargs):
        datas = response.json()["body"]
        headers = response.meta["headers"]
        pic_name = response.meta["pic_name"]
        is_many = False
        index = 1
        if len(datas) > 1:
            is_many = True
        for data in datas:
            if is_many:
                folder_name = pic_name
                pic_name = f"p{index}"
            else:
                folder_name = ""
            final_url = data["urls"]["original"]
            next_arg = {
                "pic_name": pic_name,
                "folder_name": folder_name,
                "is_many": is_many,
                "file_type": final_url.split(".")[-1]
            }
            yield Request(url=final_url, headers=headers,
                          callback=self.parse_ajax, meta=next_arg)

    def parse_ajax(self, response):
        item = PixivDownloadItem()
        image_info = response.meta
        item["title"] = image_info["pic_name"]
        item["file_type"] = image_info["file_type"]
        item["data_code"] = response.content
        item["folder_name"] = image_info["folder_name"]
        item["is_many"] = image_info["is_many"]
        yield item
