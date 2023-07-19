"""
111 - 

Author: hanayo
Date： 2023/7/19
"""

# css
<a class="classA" attr1="attr1" href="a.com">文本</a>


items = seletor.css("a.classA[attr1='attr1']")
# 获取text

# 获取href
item.attrib['href']




# xpath


item.xpath('string()').get()

pages = bs_html.find_all("div", {
    "class": "page-box house-lst-page-box",
    "comp-module": "page"
})