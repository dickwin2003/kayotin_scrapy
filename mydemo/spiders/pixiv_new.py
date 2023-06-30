"""
pixiv_new - 借助自带的ImagePipeline下载

Author: hanayo
Date： 2023/6/29
"""

import scrapy
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
import os
from mydemo.static.my_cookie import cookie, user_agent
from scrapy import Request
from mydemo.items import PixivDownloadItem


class PixivNewSpider(scrapy.Spider):
    name = "pixiv_new"
    allowed_domains = ["pixiv.net"]
    url_list = list()
    custom_settings = {
        'ITEM_PIPELINES': {
            # 如果有多条数据管道，需要在这里指定
            'mydemo.pipelines.PixivImagePipeline': 600,
        }
    }

    def start_requests(self):
        """读取Excel链接，进行请求，得到ajax请求的地址"""
        _path = os.path.abspath(os.path.dirname(__file__))
        parent_dir = os.path.dirname(_path)
        workbook = openpyxl.load_workbook(f"{parent_dir}/output/pixiv_weekly_rank数据.xlsx")  # type: Workbook
        worksheet = workbook["weekly"]  # type: Worksheet

        for row_num in range(2, worksheet.max_row + 1):
            url_obj = {
                "pic_name": f"{worksheet[f'A{row_num}'].value}_{worksheet[f'B{row_num}'].value}",
                "download_url": f"https://www.pixiv.net/ajax/illust/{worksheet[f'C{row_num}'].value}/pages?lang=zh",
                "referer": worksheet[f"D{row_num}"].value
            }
            PixivNewSpider.url_list.append(url_obj)
        workbook.close()

        for url_obj in PixivNewSpider.url_list:
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
        """将得到的下载链接和其他信息进行打包到item，让Pipeline进行处理"""
        datas = response.json()["body"]
        headers = response.meta["headers"]
        pic_name = response.meta["pic_name"]
        is_many = False
        index = 1
        if len(datas) > 1:
            is_many = True
        item = {
            "folder_name": "",
            "is_many": is_many,
            "headers": headers,
            "final_urls": [
                # {"title": pic_name, "url": "", "file_type": ""} 结构参考
            ]
        }
        for data in datas:
            img_p = {
                "title": pic_name,
                "url": data["urls"]["original"],
                "file_type": data["urls"]["original"].split(".")[-1]
            }
            if is_many:
                item["folder_name"] = pic_name
                img_p["title"] = f"p{index}"
                index += 1
            item["final_urls"].append(img_p)
        yield PixivDownloadItem(item)

