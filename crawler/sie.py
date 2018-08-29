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
            getMoreUrl(url, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            tag = soup.find('a', id='p16c4996')
            try:
                url = tag['href']
                print(url)
            except Exception as e:
                print('获取 国际教育学院 新闻地址失败')
            else:
                getMoreUrl(common.checkUrl(url))
            finally:
                pass
        finally:
            pass

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
        finally:
            pass

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
                    try:
                        times[title] = times[title] + 1
                    except Exception as e:
                        times[title] = 1
                    else:
                        pass
                    finally:
                        if not limit or times[title] <= limit:
                            print(title + '：' + str(times[title]))
                            getContent(common.checkUrl(tag['href']), title)
            finally:
                next_page = soup.find('a', class_='next')
                if next_page['href'] != 'javascript:void(0);':
                    getNewsList(common.checkUrl(next_page['href']))
        finally:
            pass

def getContent(url, bank, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find('span', class_='Article_Title').get_text().replace('  ', '')
            news_html = str(common.replaceUrl(soup.find('div', class_='Article_Content'))).replace('\'', '\\\'').replace('\"','\\\"')
            date = soup.find('span', class_='Article_PublishDate').get_text()
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getContent(url, bank,try_times = try_times+1)
        else:
            source = '国际教育学院'
            bank = '学院动态/' + bank
            news_url = url
            form = '国际教育学院'
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(source + ' ' + bank + ' ' + title + ' ' + news_url + ' ' + data + ' ' + update_time)
            # print(news_html)
            if limit:
                sql.update(source, bank, title, news_url, form, news_html, date, update_time)
            else:
                sql.save(source, bank, title, news_url, form, news_html, date, update_time)
        finally:
            pass