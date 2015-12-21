# -*- coding: utf-8 -*-
"""__author__ = 'Xiang'"""
import urllib
from bs4 import BeautifulSoup as bs
import MySQLdb


def get_html(my_url):
    page = urllib.urlopen(my_url)
    my_html = page.read()
    return my_html

url = 'http://tuijian.hao123.com/'
html = get_html(url)
soup = bs(html, 'lxml', from_encoding="utf-8")

try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='mjy123456', port=3306)
    cur = conn.cursor()
    conn.select_db('newsdb')
    for link in set(soup.find_all('a')):
        Title = unicode(link.string).strip().replace(u'\xa0', '').encode('gbk')#\xa0是HTML里的&nbsp
        print Title
        Urls = unicode(link.get('href')).encode('utf-8')
        if len(Title) <= 8 or Urls == 'http://news.sina.com.cn/' or Urls == 'javascript:' or Urls is None \
                or Urls == 'javascript:;' or Urls == 'Prev' or Urls == 'Next' or Urls == 'Left' or Urls == 'Right' \
                or Urls == 'http://data.huanqiu.com/' or Urls == 'http://humor.huanqiu.com/':
            continue

        Source = 'sina'
        Classification = 'tech'
        Title = Title.decode('gbk').encode('utf-8')#存储的时候采用utf-8

        #插入url表中
        url_value = [Source, Urls]
        try:
            cur.execute('insert into news_urlsmodel(Source, Urls) values (%s,%s)', url_value)
        except UnicodeEncodeError:
            continue
        conn.commit()

        #根据得到的url爬取新闻的概要
        detail_url = Urls
        try:
            detail_html = get_html(detail_url)
        except IOError:
            continue
        detail_soup = bs(detail_html, 'lxml', from_encoding="utf-8")
        try:
            Summary = unicode(detail_soup.p.string).strip().encode('utf-8')
        except AttributeError:
            continue

        #插入news表中
        url = cur.execute('select * from news_urlsmodel where urls=%s', Urls)
        news_value = [Title, url, Classification, Summary]
        cur.execute('insert into news_newsmodel(Title, url_id, Classification, Summary) values (%s,%s,%s,%s)', news_value)
        conn.commit()

    # cur.execute("select * from news_newsmodel where classification='tech'")
    # titles = cur.fetchall()
    # for title in titles:
    #     print title
    # print "delete from news_urlsmodel where urls='%s'" % 'http://humor.huanqiu.com/'
    # cur.execute('select * from news_urlsmodel')
    # urls = cur.fetchall()
    # for url in urls:
    #     if url[2] == 'http://data.huanqiu.com/':
    #         print url[2]
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    try:
        sqlError = "Error %d:%s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error:%s" % str(e)
