利用requests库，利用多进程抓取网站的所有图片。在mongoDB中设置了所抓取的url状态：outstanding-1,processing-2,complete-3。url在mongoDB数据库中初始状态为outstanding;从数据库取出来之后url状态为processing，在所规定的时间没有抓取到网址的内容，将url状态重置为outstanding；如果在规定的时间内能将url所对应的内容抓取到，将url状态置为complete。利用BeautifulSoup将网页中的图片地址解析出来，然后再抓取图片并放到所对应的文件夹下面。






