# kayotin_scrapy
一个练手的scrapy框架爬虫项目


## 目前包含以下爬虫
| name | 简介 |
|  | --- |
| douban | 爬取豆瓣电影 Top250 电影标题、评分和金句，保存至Excel文件 |
| pixiv | 爬取Pixiv 周榜 250 标题、作者和PID和链接，保存至Excel文件 |
| pixiv_download | 下载上一个爬虫中的图片 |
| pixiv_new | 同样是下载图片，区别是使用自定义ImagePipeline |
| shell_spider | 爬取贝壳网的二手房数据 |
| bilibili | 爬取阿b视频数据 |

## 各Spider简介

## douban

通过如下代码运行：
```python
scrapy crawl douban
```
效果：
爬取豆瓣电影 Top250 电影标题、评分和金句，保存至Excel文件

## pixiv

```python
scrapy crawl pixiv
```
效果：
爬取Pixiv 周榜 250 标题、作者和PID和链接，保存至Excel文件

## pixiv_download
```python
scrapy crawl pixiv_download
```
效果：

1. 根据上一步的数据，下载图片
2. 多p的图片保存至一个文件夹，如下所示

![pic_dic.png](mydemo%2Fstatic%2Fpic_dic.png)

## pixiv_new
```python
scrapy crawl pixiv_new
```
这个爬虫的作用和上一个相同，

但是继承了ImagePipeline自定义了Pipeline来进行下载，效率会比较高。

下载结束后，保存下载情况到Excel。

## shell_spider
```python
scrapy crawl shell_spider
```
爬取贝壳网的二手房数据，保存至excel。
5万条数据约需要运行25分钟。

## bili_spider
```python
scrapy crawl bili_spider
```

爬取指定av号的视频，比如av10000-av12000

但是可能会被阿b检测到然后禁ip
谨慎使用