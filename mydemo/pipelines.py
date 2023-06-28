# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class MydemoPipeline:
#     def process_item(self, item, spider):
#         return item

import openpyxl
from mydemo.items import DoubanItem, PixivItem, PixivDownloadItem
import os


class DoubanItemPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = 'Top250'
        self.sheet.append(('名称', '评分', '名言'))

    def process_item(self, item: DoubanItem, spider):
        self.sheet.append((item['title'], item['score'], item['motto']))
        return item

    def close_spider(self, spider):
        # 获取根目录路径
        root_path = os.path.abspath(os.path.dirname(__file__))
        self.wb.save(f'{root_path}/output/豆瓣电影数据.xlsx')


class PixivPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = 'weekly'
        self.sheet.append(('标题', '作者', 'P_ID', "链接"))

    def process_item(self, item: PixivItem, spider):
        self.sheet.append((item['title'], item['user_name'], item['p_id'], item['re_url']))
        return item

    def close_spider(self, spider):
        # 获取根目录路径
        root_path = os.path.abspath(os.path.dirname(__file__))
        self.wb.save(f'{root_path}/output/pixiv_weekly_rank数据.xlsx')


class PixivDownloadPipeline:
    images_folder = 'path/to/your/images/folder'

    def process_item(self, item, spider):
        # 检查Item是否包含图片URL
        if 'image_urls' in item and len(item['image_urls']) > 0:
            for image_url in item['image_urls']:
                # 生成下载请求，并指定回调函数
                request = scrapy.Request(image_url, callback=self.handle_downloaded_image)
                request.meta['item'] = item
                spider.crawler.engine.schedule(request, spider)
        else:
            raise DropItem("Item does not contain image URLs")
        return item

    def handle_downloaded_image(self, response):
        # 在这里处理下载后的图片，例如保存到本地
        item = response.meta['item']
        image_path = os.path.join(self.images_folder, item['name'] + '.jpg')

        with open(image_path, 'wb') as f:
            f.write(response.body)

        # 如果需要，可以将下载后的图片路径添加到Item中
        item['image_path'] = image_path