#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re
import time
from common import sql, common

limit = 0
times = {}

def start(url, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            start(url, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            tag = soup.find('a', id='p16c4996')
            try:
                url = tag['href']
                # print(url)
            except Exception as e:
                print('获取 国际教育学院 新闻地址失败')
            else:
                getMoreUrl(common.checkUrl(url))

def getMoreUrl(url, try_times = 1):
    if try_times <= 3:
        try:
            # print(url)
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getMoreUrl(url, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            menuTag = soup.find('div', class_='submenu')
            tags = menuTag.find_all('a')
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
                tags = soup.find('div',id='wp_news_w3').find_all('a')
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
                        getContent(common.checkUrl(tag['href']), title)
                if not limit or times[title] < limit:
                    next_page = soup.find('a', class_='next')
                    if next_page != None:
                        if next_page['href'] != 'javascript:void(0);':
                            getNewsList('http://www2.scut.edu.cn' + next_page['href'])

def getContent(url, bank, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find('span', class_='Article_Title').get_text().replace('  ', '')
            news_html = str(common.replaceUrl(soup.find('div', class_='Article_Content'))).replace('\'', '\\\'').replace('\"','\\\"')
            date = soup.find('span', class_='Article_PublishDate').get_text()
            form_tag = soup.find('a', title='原文')
            if form_tag != None:
                form = form_tag.get_text()
            else:
                form = '国际教育学院'
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getContent(url, bank,try_times = try_times+1)
            result = True
        else:
            source = '国际教育学院'
            bank = '学院动态/' + bank
            news_url = url
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