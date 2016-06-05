# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pymongo
import time
import random

#初始化数据库，一些数据库为调试用，，需要用到的是movie_links,movie_only_links,movie_information_review
client = pymongo.MongoClient('localhost',27017)
tencetn_moive = client['tencetn_moive']
moive_link = tencetn_moive['moive_link']
#用于存放从网上爬取的所有url
movie_links = tencetn_moive['moive_links']
movie_information = tencetn_moive['movie_information']
#将movie_links去重后加入movie_only_links
movie_only_links = tencetn_moive['movie_only_links']
movie_information_full = tencetn_moive['movie_information_full']
movie_label = tencetn_moive['movie_label']
movie_information_tall = tencetn_moive['movie_information_tall']
#存放影片信息
movie_information_review = tencetn_moive['movie_information_review']

#腾讯电影主页
url_main = 'http://v.qq.com/movie/'
type_link = []

#Cookie
header = {
    'Cookie':'RK=06+qjuKXfg; pgv_pvi=5469034496; ptui_loginuin=1138426807; ptcz=e38636938111699937a12ff35293f6e87cc84c64074c3f5f9209becd557a7276; pt2gguin=o1138426807; pgv_info=ssid=s5270185427; pgv_pvid=5959977926; o_cookie=1138426807',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}

#虚拟IP
proxy_list = [
    'http://103.38.42.132:80',
    'http://58.22.191.243:80',
    'http://123.59.101.100:80',
    'http://120.52.72.19:80',
    'http://182.48.106.18:80',
    'http://223.68.190.132:8000',
    'http://116.242.19.241:3128',

    ]
proxy_ip = random.choice(proxy_list)
proxies = {'http':proxy_ip}

#类型页面的url
def get_type_url(url):
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.text,'lxml')
    links = soup.select('.filter_item_type .filter_list a')
    for link in links:
        type_link.append(link.get('href'))
    #print(title[0].get('href'))
    #href = re.findall(r'href="(.*?)"',str(title[0]),re.S)
    #print(href)
    #return href


# def get_movie_url(url):
#     web_page = requests.get(url,headers = header)
#     soup = BeautifulSoup(web_page.text,'lxml')
#     links = soup.select('.figures_list .figure')
#     for link in links:
#         moive_link.insert_one({'url':link.get('href')})
#         #print(link.get('href'))

#获取各个网页中电影的url
def get_more_movie_url(url,page):
    movie_links.remove()
    page_num = [i for i in range(0,page*20,20)]
    page_url_list = []
    #print(type_link)
    for link in type_link:
        for pages in page_num:
            #print(pages)
            page_url = re.sub('offset(.*?)&','offset='+str(pages)+'&',link,re.S)
            page_url_list.append(page_url)
    print(page_url_list)
    for url in page_url_list:
        web_page = requests.get(url,proxies=proxies)
        soup = BeautifulSoup(web_page.text,'lxml')
        if soup.find(class_='page_btn_disable'):
            pass
        else:
            movies_link = soup.select('.figure_title a')
            for moive_link in movies_link:
                #time.sleep(1)
                movie_links.insert_one({'url':moive_link.get('href')})
                #print(moive_link.get('href'))
            #print(moive_link.get('href'))



#爬取各种类型第一页到第一百页的电影url,
#movie_links.remove()
# start = time.time()
# get_type_url(url_main)
# get_more_movie_url(1,100)
# print(movie_links.count())
# print(len(movie_links.distinct('url')))
# for i in movie_links.distinct('url'):
#     print(i)
#     movie_only_links.insert_one({'url':i})
# print(movie_only_links.count())
# print(time.time() - start)
'''
moive_link.remove()
get_movie_url('http://v.qq.com/x/movielist/?cate=10001&offset=0&sort=5&pay=-1&area=-1&subtype=100062')
'''
'''
href = get_type_url(url_main)
print(href)
'''


#print(movie_only_links.count())

# list = []
# for i in movie_information_review.find():
#     #print (i['label'])
#     list.append(i['label'])
# print(list)






