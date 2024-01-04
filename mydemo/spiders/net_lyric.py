"""
net_lyric - 爬取歌曲评论

https://music.163.com/api/v1/resource/comments/R_SO_4_536624574?limit=20&offset=0
评论是comments
热评是hotComments

Author: hanayo
Date： 2024/1/4
"""

import scrapy
import requests
from mydemo.static.my_cookie import net_cookie, user_agent
import os
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
import json
from mydemo.items import NetWordItem


def read_from_excel():
    _path = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(_path)
    workbook = openpyxl.load_workbook(f"{parent_dir}/output/net_music_data.xlsx")  # type: Workbook
    worksheet = workbook["网易云"]  # type: Worksheet

    for row_idx in range(2, worksheet.max_row + 1):
        song_name = worksheet[f"A{row_idx}"].value
        song_id = worksheet[f"D{row_idx}"].value.split("=")[-1]
        song_url = f"https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}"
        yield {
            'song_name': song_name,
            'song_url': song_url
        }


class LyricSpider(scrapy.Spider):
    name = "net_lyric"
    allowed_domains = ["www.163.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'mydemo.pipelines.NetWordItemPipeline': 900,
        }
    }
    headers = {
        'User-Agent': user_agent,
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/'
    }

    def start_requests(self):
        songs = read_from_excel()
        for song in songs:
            yield scrapy.Request(url=song["song_url"], headers=self.headers, meta={"song_name": song["song_name"]})

    def parse(self, response, **kwargs):
        res_dict = json.loads(response.body)
        for con in res_dict["hotComments"]:
            item = {
                "song_name": response.meta["song_name"],
                "user_name": con['user']['nickname'],
                "content": con['content'],
                "comment_date": con['timeStr'],
                "liked_count": con['likedCount']
            }
            yield NetWordItem(item)


if __name__ == '__main__':
    # test_url = "https://music.163.com/api/v1/resource/comments/R_SO_4_536624574"
    # res = requests.get(test_url)
    # json_res = res.json()
    # print(len(json_res["hotComments"]))
    # for con in json_res["hotComments"]:
    #     print(f"用户名：{con['user']['nickname']}，评论内容：{con['content']}, "
    #           f"评论时间：{con['timeStr']}, 点赞数：{con['likedCount']}")
    pass
