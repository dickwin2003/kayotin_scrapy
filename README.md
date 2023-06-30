# mydemo
一个练手的scrapy框架爬虫项目




### 主要功能

通过如下代码运行：
```python
scrapy crawl douban
```
效果：
爬取豆瓣电影 Top250 电影标题、评分和金句，保存至Excel文件

```python
scrapy crawl pixiv
```
效果：
爬取Pixiv 周榜 250 标题、作者和PID和链接，保存至Excel文件


```python
scrapy crawl pixiv_download
```
效果：

1. 根据上一步的数据，下载图片
2. 多p的图片保存至一个文件夹，如下所示

![pic_dic.png](mydemo%2Fstatic%2Fpic_dic.png)


```python
scrapy crawl pixiv_new
```
这个爬虫的作用和上一个相同，

但是继承了ImagePipeline自定义了Pipeline来进行下载，效率会比较高。

下载结束后，保存下载情况到Excel。