#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql

# print('sql')

db = pymysql.connect('localhost', 'root', 'root', 'scut_news')

def save(source, bank, title, news_url, form, news_html, date, update_time):
    global db
    cursor = db.cursor()
    sql = "INSERT INTO scut_news (source, bank, title, news_url, form, news_html, date, update_time) \
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s' ,'%s' ,'%s')" % \
        (source, bank, title, news_url, form, news_html, date, update_time)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    else:
        pass
    finally:
        pass

def update(source, bank, title, news_url, form, news_html, date, update_time):
    global db
    cursor = db.cursor()
    sql = "SELECT * FROM scut_news \
        WHERE news_url = '%s'" % (news_url)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        if len(results) == 0:
            save(source, bank, title, news_url, form, news_html, date, update_time)
    except Exception as e:
        print(e)
    else:
        pass
    finally:
        pass
