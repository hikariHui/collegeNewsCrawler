#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

def replaceUrl(content):
    try:
        tags = content.find_all('img')
        for tag in tags:
            # print(tag['src'])
            if tag['src'] != '' and not re.search(r'http(s)?://', tag['src']):
                tag['src'] = 'http://www2.scut.edu.cn' + tag['src']
                # print(tag['src'])

        tags = content.find_all('a')
        for tag in tags:
            # print(tag['href'])
            if tag['href'] != '' and tag['href'] != 'javascript:void(0);' and not re.search(r'http(s)?://', tag['href']):
                tag['href'] = 'http://www2.scut.edu.cn' + tag['href']
                # print(tag['href'])

        tags = content.find_all('div',class_='wp_video_player')
        for tag in tags:
            if tag['sudy-wp-src'] != '':
                tag.name = 'video'
                tag['src'] = 'http://www2.scut.edu.cn' + tag['sudy-wp-src']
                tag['controls'] = 'controls'
                # print(content)
    finally:
        return content

def checkUrl(url):
    if not re.search(r'http(s)?://', url):
        url = 'http://www2.scut.edu.cn' + url
    return url