#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib.request
from crawler import bmse, sie, med, lifesciences

college_url = {
    'bmse': 'http://www2.scut.edu.cn/bmse/', # 生物医学科学与工程学院
    'sie': 'http://www2.scut.edu.cn/sie_cn/', # 国际教育学院
    'med': 'http://www2.scut.edu.cn/med/', # 医学院
    'lifesciences': 'http://www2.scut.edu.cn/lifesciences/', # 生命科学研究院
    'design': 'http://www.scut.edu.cn/design/', # 设计学院 (失效)
    'sport': 'http://202.38.194.171/sport/' # 体育学院
}

def main():
    global college_url
    # print('生物医学科学与工程学院')
    # bmse.limit = 5
    # bmse.start(college_url['bmse'])
    # print('国际教育学院')
    # sie.limit = 5
    # sie.start(college_url['sie'])
    # print('医学院')
    # med.limit = 5
    # med.start(college_url['med'])
    # print('生命科学研究院')
    # lifesciences.limit = 5
    # lifesciences.start(college_url['lifesciences'])
    # print('设计学院')
    # design.limit = 5
    # design.start(college_url['design'])
    # print('体育学院')
    # sport.limit = 5
    # sport.start(college_url['sport'])

main()