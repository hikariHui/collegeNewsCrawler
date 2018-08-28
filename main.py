#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
from crawler import bmse

college_url = {
    'bmse': 'http://www2.scut.edu.cn/bmse/' # 生物医学科学与工程学院
}

def main():
    global college_url
    # print(college_url['bmse'])
    bmse.start(college_url['bmse'])

main()