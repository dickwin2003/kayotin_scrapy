# kayotin_scrapy
一个练手的scrapy框架爬虫项目
--在源代码上增加了一个采集任务 可看日期
huxiu_spider.py

## 目前包含以下爬虫
| name           | 简介                                     |
|----------------|----------------------------------------|
| douban         | 爬取豆瓣电影 Top250 电影标题、评分和金句，保存至Excel文件    |
| pixiv          | 爬取Pixiv 周榜 250 标题、作者和PID和链接，保存至Excel文件 |
| pixiv_download | 下载上一个爬虫中的图片                            |
| pixiv_new      | 同样是下载图片，区别是使用自定义ImagePipeline          |
| shell_spider   | 爬取贝壳网的二手房数据                            |
| bili_spider    | 爬取阿b视频数据                               |
| net_spider     | 爬取网易云指定歌单歌曲信息                          |
| net_lyric      | 爬取net_spider爬取到的歌单中的歌曲热评               |



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

## net_spider
```python
scrapy crawl net_spider
```

爬取指定歌单id的所有歌曲信息，

由于歌单是需要登录才能访问的，目前需要在static/my_cookie.py中指定cookie值，

目前是我的歌单，如果要爬取其他歌单，修改如下id即可

play_list_id = "478849060"

## net_lyric
```python
scrapy crawl net_lyric
```

爬取上一个歌单中的所有歌曲的热门评论，

因为是从excle文件读取的，所以运行前请确保上一个爬虫生成的excle文件存在

结果同样保存在excle中
