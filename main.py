#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
from crawler import bmse, sie

college_url = {
    'bmse': 'http://www2.scut.edu.cn/bmse/', # 生物医学科学与工程学院
    'sie': 'http://www2.scut.edu.cn/sie_cn/' # 国际教育学院
}

def main():
    global college_url
    # bmse.limit = 5
    # bmse.start(college_url['bmse'])
    # sie.limit = 5
    sie.start(college_url['sie'])

main()