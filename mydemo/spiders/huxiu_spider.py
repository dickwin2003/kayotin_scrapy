#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : Spider for scraping content from tab_contet_dx elements
"""
import scrapy
from mydemo.items import HuxiuItem

class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["k366.com"]
    start_urls = [f"https://cm.k366.com/qian/lqhdx_{i}.htm" for i in range(1, 4)]
    sql_statements = []  # To store all SQL statements

    def parse(self, response):
        # 从URL中提取页码
        page_number = int(response.url.split('_')[-1].split('.')[0])
        tab_contents = response.css('.tab_contet_dx')
        contents = []
        
        # Extract first content (xj)
        content1 = tab_contents[0].css('::text').get().strip() if len(tab_contents) >= 1 else ''
        contents.append(content1)
        
        # Extract second content (qs)
        if len(tab_contents) >= 2:
            content2_list = tab_contents[1].css('p::text').getall()
            content2 = ' '.join(text.strip() for text in content2_list if text.strip())
        else:
            content2 = ''
        contents.append(content2)
        
        # Extract third content (jy)
        content3 = tab_contents[2].css('::text').get().strip() if len(tab_contents) >= 3 else ''
        contents.append(content3)
        
        # Extract fourth content (xj)
        if len(tab_contents) >= 4:
            content4_list = tab_contents[3].css('p::text').getall()
            content4 = ' '.join(text.strip() for text in content4_list if text.strip())
        else:
            content4 = ''
        contents.append(content4)
        
        # Extract fifth content (dg)
        content5 = tab_contents[4].css('::text').get().strip() if len(tab_contents) >= 5 else ''
        contents.append(content5)

        # 转义单引号，防止SQL语句出错
        contents = [c.replace("'", "''") for c in contents]

        # Generate SQL insert statement with page number
        sql = f"INSERT INTO t_hdx (no, jx, qs, jy, xj, dg) VALUES ({page_number}, '{contents[0]}', '{contents[1]}', '{contents[2]}', '{contents[3]}', '{contents[4]}');"
        
        # Append the SQL statement to our collection
        self.sql_statements.append(sql)
        
        yield {
            'sql': sql
           # 'data': contents
        }

    def closed(self, reason):
        # Combine all SQL statements with semicolons and newlines
        combined_sql = '\n'.join(self.sql_statements)
        
        # 输出到控制台，方便复制
        print("\n=== 合并后的SQL语句开始 ===")
        print(combined_sql)
        print("=== 合并后的SQL语句结束 ===\n")
        
        # 同时保存到文件
        with open('combined_sql.sql', 'w', encoding='utf-8') as f:
            f.write(combined_sql)