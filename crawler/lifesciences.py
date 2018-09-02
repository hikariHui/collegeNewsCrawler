#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re
import time
from common import sql, common

limit = 0
times = {}

def getMoreUrl(url, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getMoreUrl(url, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all('a', class_='more')
            for tag in tags:
                getNewsList(common.checkUrl(tag['href']))
            for key in times:
                print(key + '：' + str(times[key]))

def getNewsList(url, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getNewsList(url, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find('title').get_text()
            # tags = soup.find_all('a', class_='more')
            try:
                tags = soup.find('ul',class_='wp_article_list').find_all('li')
            except Exception as e:
                pass
            else:
                for tag in tags:
                    # print(title)
                    if title not in times:
                        times[title] = 0
                    if not limit or times[title] < limit:
                        # print(title + '：' + str(times[title]))
                        times[title] = times[title] + 1
                        getContent('http://www2.scut.edu.cn' + tag.find('a')['href'], title, tag.find('span', class_='Article_PublishDate').get_text())
                if not limit or times[title] < limit:
                    next_page = soup.find('a', class_='next')
                    if next_page != None:
                        if next_page['href'] != 'javascript:void(0);':
                            getNewsList('http://www2.scut.edu.cn' + next_page['href'])

def getContent(url, bank, date, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find('span', class_='news_title').get_text().replace('  ', '')
            news_html = str(common.replaceUrl(soup.find('div', class_='Article_Content'))).replace('\'', '\\\'').replace('\"','\\\"')
            form_tag = soup.find('a', title='原文')
            if form_tag != None:
                form = form_tag.get_text()
            else:
                form = '生命科学研究院'
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getContent(url, bank, date, try_times = try_times+1)
            result = True
        else:
            source = '生命科学研究院'
            bank = bank
            news_url = url
            date = date
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(source + ' ' + bank + ' ' + title + ' ' + news_url + ' ' + data + ' ' + update_time)
            # print(news_html)
            if limit:
                result = sql.update(source, bank, title, news_url, form, news_html, date, update_time)
            else:
                result = sql.save(source, bank, title, news_url, form, news_html, date, update_time)
    else:
        result = False
    if not result:
        times[bank] = times[bank] - 1

start = getMoreUrl