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
            tags = {}
            tags['学院信息'] = soup.find('a', string='学院信息')
            tags['新闻中心'] = soup.find('a', string='新闻中心')
            tags['研究成果'] = soup.find('a', string='研究成果')
            tags['学生工作'] = soup.find('a', title='学生工作')
            for key in tags:
                try:
                    url = tags[key]['href']
                    print(url)
                except Exception as e:
                    print('获取 医学院 %s 地址失败' % (key))
                else:
                    getMoreUrl(common.checkUrl(url), key)
                finally:
                    pass
        finally:
            pass

def getMoreUrl(url, bank, try_times = 1):
    if try_times <= 3:
        try:
            # print(url)
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getMoreUrl(url, bank, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            menuTag = soup.find('ul', class_='wp_listcolumn')
            tags = menuTag.find_all('a')
            if len(tags) == 0:
                getNewsList(url, bank)
            else:
                for tag in tags:
                    try:
                        getNewsList(common.checkUrl(tag['href']), bank + '/' + tag['title'])
                    except Exception as e:
                        pass
                    else:
                        pass
                    finally:
                        pass
        finally:
            pass

def getNewsList(url, bank, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getNewsList(url, bank, try_times = try_times+1)
        else:
            soup = BeautifulSoup(html, "html.parser")
            # bank = bank + '/' + title
            # tags = soup.find_all('a', class_='more')
            try:
                tags = soup.find('div',id='wp_news_w10').find_all('a')
            except Exception as e:
                pass
            else:
                for tag in tags:
                    # print(bank)
                    try:
                        times[bank] = times[bank] + 1
                    except Exception as e:
                        times[bank] = 1
                    else:
                        pass
                    finally:
                        if not limit or times[bank] <= limit:
                            print(bank + '：' + str(times[bank]))
                            getContent(common.checkUrl(tag['href']), bank)
                if not limit or times[bank] <= limit:
                    next_page = soup.find('a', class_='next')
                    if next_page != None:
                        if next_page['href'] != 'javascript:void(0);':
                            getNewsList(common.checkUrl(next_page['href']), bank)
        finally:
            pass

def getContent(url, bank, try_times = 1):
    if try_times <= 3:
        try:
            html = urllib.request.urlopen(url).read().decode(encoding='utf-8')
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find('div', class_='mainTitles').find('h1').get_text().replace('  ', '')
            news_html = str(common.replaceUrl(soup.find('div', class_='wp_articlecontent'))).replace('\'', '\\\'').replace('\"','\\\"')
            date = re.search(r'日期：(\d+-\d+-\d+)', soup.find('div', class_='mainTitles').find('h3').get_text()).group(1)
            form_tag = soup.find('a', title='原文')
            if form_tag != None:
                form = form_tag.get_text()
            else:
                form = '医学院'
        except Exception as e:
            print('错误URL：' + url)
            print(e)
            print('进行第%d次尝试'%(try_times+1))
            getContent(url, bank,try_times = try_times+1)
        else:
            source = '医学院'
            bank = bank
            news_url = url
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # print(source + ' ' + bank + ' ' + title + ' ' + news_url + ' ' + data + ' ' + update_time)
            # print(news_html)
            if limit:
                sql.update(source, bank, title, news_url, form, news_html, date, update_time)
            else:
                sql.save(source, bank, title, news_url, form, news_html, date, update_time)
        finally:
            pass