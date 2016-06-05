# -*- coding: utf-8 -*-

'''
本段代码主要从get_url中读取之前存放好电影url的数据库，然后通过url爬取数据信息
'''

import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from get_url import movie_only_links,header,movie_information_tall,proxies,movie_information_review
import re
import time
import json


#腾讯视频点开分两种，一种是qq电影，另一种是好莱坞影院，两者需要区分爬取
def classify(url):
    try:
        #使用requests请求
        web_page = requests.get(url)
        web_page.encoding = 'utf-8'
        #使用BeautifulSoup读取url信息
        soup = BeautifulSoup(web_page.text,'lxml')
        if soup.find(class_='site_logo') == None:
            #好莱坞影院
            get_Hollywood_video_information(url)
            #print(url)
        else:
            #qq电影
            get_qq_video_information(url)
            #print(url)
    except:
        print('except')


#因为分数是存在JS当中，所以需要单独写代码爬取
def get_score(url):
    #使用正则表达式匹配出新的url
    url_taile = url.split('/')[5]
    url_taile = re.findall(r'(.*?)\.html',url_taile,re.S)
    url_score = 'http://data.video.qq.com/fcgi-bin/data?tid=128&appid=10001007&appkey=e075742beb866145&idlist={}&otype=json'.format(url_taile[0])
    #print(url_score)
    try:

        web_page = requests.get(url_score).text
        #print(web_page)
        #time.sleep(10)
		#使用正则表达式查找score
        score = re.findall(r'"score":"(.*?)"}},',web_page,re.S)
        if len(score) == 0:
            print(url)
            pass
        else:
            return score[0]
    except:
        print('except')

#好莱坞影院导演和演员的信息是在JS中，需要单独写代码
def get_director_actor(url):
    url_data_tail = url.split('/')[5]
    #print(url_data_tail)
    url_data_tail = re.findall(r'(.*).html',url_data_tail,re.S)
    #print(url_data_tail)
    url_data = 'http://data.video.qq.com/fcgi-bin/data?tid=205&appid=20001059&appkey=c8094537f5337021&otype=json&idlist={}'.format(url_data_tail[0])
    try:
        web_page = requests.get(url_data)
        #time.sleep(10)
        soup = BeautifulSoup(web_page.text,'lxml')
        director = re.findall(r'"director":\["(.*?)"\]',str(soup),re.S)
        actor = re.findall(r'"leading_actor":\[(.*?)\]',str(soup),re.S)
        actors = re.findall(r'"(.*?)"',actor[0],re.S)
        return director,actors
    except:
        print('except')

#爬取qq电影信息
def get_qq_video_information(url):
    try:
        web_page = requests.get(url,headers = header)
        #time.sleep(6)
        web_page.encoding = 'utf-8'
        soup = BeautifulSoup(web_page.text,'lxml')
        #电影标题
        titles = soup.select('.breadcrumb_item')
        #电影标签
        labels = soup.select('.tag_list')
        #电影导演
        directors = soup.select('#mod_descContent > ul > li:nth-of-type(2) > div > div > ul > li > a > span')
        #电影演员
        actors = soup.select('#mod_descContent > ul > li:nth-of-type(3) > div > div > ul')

        if (len(titles) == 0) or (len(labels) == 0) or (len(directors) == 0) or (len(actors) == 0):
            print(url)
            pass
        else:
            title = titles[0].text
            label = re.findall(r'title="(.*?)"',str(labels[0]),re.S)
            score = get_score(url)
            #获取hot评论和一般评论
            hot_review,review = get_qq_reviews(url)
            director = directors[0].text
            actor = actors[0]
            actor_name = re.findall(r'title="(.*?)"',str(actor),re.S)

            data = {'title':title,
                    'label':label,
                    'score':score,
                    'director':director,
                    'actor':actor_name,
                    'hot_review':hot_review,
                    'review':review
            }

            movie_information_review.insert_one(data)
            print(data)
    except:
        print('except')

def get_Hollywood_video_information(url):
    #匹配出好莱坞影院的url(好莱坞影院的url不是现成的)
    url_real = url.split('/')[4] + '/' + url.split('/')[5]
    #print(url_real)
    url_real = 'http://film.qq.com/cover/{}?ADTAG=INNER.TXV.COVER.REDIR'.format(url_real)
    #print(url_real)
    try:
        web_page = requests.get(url_real,headers = header)
        #防止访问过快在爬好莱坞影院时候休息六秒
        time.sleep(6)
        web_page.encoding = 'utf-8'
        soup = BeautifulSoup(web_page.text,'lxml')
        titles = soup.select('.title_cn')
        labels = soup.select('.tag_list a span')
        years = soup.select('body > div.site_container > div > div:nth-of-type(2) > div > div.intro_lt > div.detail_list > div.type > span:nth-of-type(2) > a')
        scores = soup.select('.score')
        hot_review,review = get_qq_reviews(url_real)
        if len(titles)==0 or len(labels)==0 or len(years)==0 or len(scores)==0 or len(hot_review)==0 or len(review)==0:
            print(url)
            pass
        else:
            title = titles[0].text
            label = [label.text for label in labels]
            year = years[0].text
            director,actor = get_director_actor(url)
            score = scores[0].text
            data = {
                'title':title,
                'label':label,
                'year':year,
                'director':director,
                'actor':actor,
                'score':score,
                'hot_review':hot_review,
                'review':review
            }
            #movie_information_tall.insert_one(data)
            movie_information_review.insert_one(data)
            print(data)
    except :
        print('except')
        pass

#爬取评论，qq电影和好莱坞电影的评论url匹配方式是相同的
def get_qq_reviews(url):
    url_data_tail = url.split('/')[5]
    url_data_tail = re.findall(r'(.*).html',url_data_tail,re.S)
    url_id = 'http://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&cid={}'.format(url_data_tail[0])
    try:
        web_id = requests.get(url_id,headers = header).text
        #print(url_id)
        id = re.findall(r'"comment_id":"(.*?)"',web_id,re.S)[0]
        #print(id)
        web_hot_comment = 'http://video.coral.qq.com/article/{}/hotcomment'.format(id)
        web_comment = 'http://coral.qq.com/article/{}/comment'.format(id)
        #print(web_hot_comment)
        #print(web_comment)
        try:
            page_hot_comment = requests.get(web_hot_comment,headers = header).text
            page_comment = requests.get(web_comment,headers = header).text

            js_hot_direct = json.loads(page_hot_comment)
            js_hot_reviews = js_hot_direct['data']['commentid']
            js_hot_reviews = [reviews['content'] for reviews in js_hot_reviews]
            js_direct = json.loads(page_comment)
            js_reviews = js_direct['data']['commentid']
            js_reviews = [reviews['content'] for reviews in js_reviews]
            return js_hot_reviews,js_reviews
        except:
            print('except')
            pass
    except:
        print('except')
        pass

#主函数
# if __name__ == "__main__":
      #清空数据库
#     movie_information_review.remove()
#     movie_link = []
#     for i in movie_only_links.find():
#         movie_link.append(i['url'])
      #初始化进程池
#     pool = Pool()
      #多进程爬取
#     pool.map(classify,movie_link)
#     pool.close()
#     pool.join()

#输出数据库内容
# for i in movie_information_review.find():
#     print(i)

#输出数据库条数
#print(movie_information_review.count())

