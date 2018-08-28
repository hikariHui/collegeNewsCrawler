#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re
import time
from crawler import sql

def getMoreUrl(url):
    try:
        html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
    except Exception as e:
        print('错误URL：' + url)
    else:
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find_all('a', class_='more')
        for tag in tags:
            getNewsList(tag['href'])
    finally:
        pass

def getNewsList(url):
    try:
        html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
    except Exception as e:
        print('错误URL：' + url)
    else:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find('title').get_text()
        # tags = soup.find_all('a', class_='more')
        try:
            tags = soup.find('ul',class_='list-wrap row').find_all('a')
        except Exception as e:
            pass
        else:
            for tag in tags:
                # print(title)
                getContent('http://www2.scut.edu.cn' + tag['href'], title)
        finally:
            pass
    finally:
        pass

def getContent(url, bank):
    try:
        html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
    except Exception as e:
        print('错误URL：' + url)
    else:
        soup = BeautifulSoup(html, "html.parser")
        source = '生物医学科学与工程学院'
        bank = '新闻动态/' + bank
        title = soup.find('div', class_='artcle-title').get_text().replace('  ', '')
        news_url = url
        form = '生物医学科学与工程学院'
        news_html = str(replaceUrl(soup.find('div', class_='Article_Content'))).replace('\'', '\\\'').replace('\"','\\\"')
        date = re.search(r'发布时间：(\d+-\d+-\d+)', soup.find('div', class_='artcle-message').get_text()).group(1)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(source + ' ' + bank + ' ' + title + ' ' + news_url + ' ' + data + ' ' + update_time)
        # print(news_html)
        sql.save(source, bank, title, news_url, form, news_html, date, update_time)
    finally:
        pass

def replaceUrl(content):
    try:
        tags = content.find_all('img')
        for tag in tags:
            if tag['src'] != '':
                tag['src'] = 'http://www2.scut.edu.cn' + tag['src']
    except Exception as e:
        pass
    else:
        return content
    finally:
        pass

start = getMoreUrl