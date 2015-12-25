# -*- coding: utf-8 -*-
# __author__ = 'Xiang'
import urllib
from bs4 import BeautifulSoup as bs
import MySQLdb
import lxml


def get_html(my_url):
    """
    获得网页的html
    :param my_url: 网页链接
    :return:
    """
    page = urllib.urlopen(my_url)
    my_html = page.read()
    return my_html


def delete():
    """
    删除数据
    :return:
    """
    conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
    cur = conn.cursor()
    conn.select_db('newsdb')
    cur.execute('SET foreign_key_checks=0')
    cur.execute('truncate table news_urlsmodel')
    cur.execute('truncate table news_newsmodel')
    cur.execute('SET foreign_key_checks=1')
    cur.close()
    conn.close()


def show_data():
    """
    查看数据库中的数据
    :param cur: 数据库操作的cursor
    :return:
    """
    conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
    cur = conn.cursor()
    conn.select_db('newsdb')
    cur.execute('SET NAMES utf8;')

    # cur.execute('select * from news_urlsmodel')
    # urls = cur.fetchall()
    # for url in urls:
    #     print url

    cur.execute('select * from news_newsmodel')
    news = cur.fetchall()
    for new in news:
        print 'title'
        print new[1].decode('utf-8').encode('gbk', 'ignore')
        print 'sum'
        print new[3].decode('utf-8').encode('gbk', 'ignore')
        print 'image'
        if new[4].decode('utf-8').encode('gbk', 'ignore') == ' ':
            print 1
        elif new[4].decode('utf-8').encode('gbk', 'ignore') == '_':
            print 2


def merge(cur, title_):
    """
    整合新闻
    :param cur: 数据库操作的cursor
    :param title_: 需要整合的新闻的链接
    :return:
    """
    cur.execute('select * from news_newsmodel')
    news_set = cur.fetchall()  # 所有和需要整合的新闻的集合
    title_set = title_.split()  # 需要整合的新闻的标题出现的字的集合
    # print 'title'
    # print title_.decode('utf-8').encode('gbk', 'ignore')
    for news_ in news_set:
        # print news_[1].decode('utf-8').encode('gbk', 'ignore')
        news_title_set = news_[1].split()  # 数据库中的新闻的标题出现的字的集合
        count = 0
        for item in title_set:
            if item in news_title_set:
                count += 1
        similarity = 1.0 * count / len(title_set)
        if similarity > 0.5:
            print "return"
            print news_
            return news_, similarity  # 直接返回这个新闻和相似度
    return None, 0


class Bugger:
    def __init__(self, url_=None, classfication_=None, source_=None, news_class_=None, image_class_=None):
        self.url = url_
        try:
            self.html = get_html(self.url)
        except IOError:
            return
        # print self.html
        self.soup = bs(self.html, 'lxml')
        # print self.soup.original_encoding
        self.classification = classfication_
        self.source = source_
        self.news_class = news_class_
        self.image_class = image_class_

        if self.source == 'sina':
            self.scripy_sina()
            print 'sina'
        elif self.source == '163':
            self.scripy_163()
            print '163'
        elif self.source == 'sohu':
            self.scripy_sohu()
            print 'sohu'

    def scripy_sina(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
            cur = conn.cursor()
            conn.select_db('newsdb')
            cur.execute('SET NAMES utf8;')

            # 爬取网页信息
            news = self.soup.find('div', class_=self.news_class)

            # 有可能网页链接不上，只有连接上了才能爬取数据
            if news is not None:
                for div in news.find_all('div'):
                    for link in div.find_all('a'):
                        try:
                            if len(link.string) == 0:  # 标题为空的不要存
                                continue
                        except TypeError:
                            continue

                        # 获取标题和链接
                        title = unicode(link.string).strip().encode('utf-8')
                        urls = unicode(link.get('href')).strip().encode('utf-8')

                        # 先判断爬取到的url是否已经存到数据库中
                        cur.execute('select * from news_urlsmodel where Urls = %s', urls)
                        url_set = cur.fetchall()
                        if len(url_set) > 0:  # 说明爬取到的url已经存在了
                            continue

                        # 整合新闻
                        similar_news, similarity = merge(cur, title)
                        if similar_news is not None:  # 非空表示新闻可以整合，为空表示没有相似的新闻，直接执行后面的
                            if similarity == 1.0:  # 新闻重复了
                                cur.execute('select * from news_urlsmodel where News_id = %s', similar_news[0])
                                similar_url_set = cur.fetchall()
                                for similar_url in similar_url_set:
                                    if similar_url[2] == urls:  # 如果url已经存在，那么就不存，否则存
                                        continue
                                # 如果url不存在，那么就存
                                url_value = [self.source, urls, similar_news[0]]
                                cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)',
                                            url_value)
                                continue
                            else:  # 整合新闻
                                url_value = [self.source, urls, similar_news[0]]
                                cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)',
                                            url_value)
                                continue

                        # 根据得到的url爬取新闻的概要,如果能爬到新闻的概要才存到数据库中
                        detail_url = urls
                        try:
                            detail_html = get_html(detail_url)
                        except IOError:
                            continue

                        detail_soup = bs(detail_html, 'lxml')
                        detail_news = detail_soup.find_all('div', id='artibody')

                        # 寻找摘要
                        flag = 0
                        for detail_div in detail_news:
                            for detail_p in detail_div.find_all('p'):
                                p = detail_p.string
                                try:
                                    if len(p) >= 50:
                                        summary = p
                                        flag = 1  # flag等于1表示存在满足条件的摘要，跳出循环
                                        break
                                except TypeError:
                                    continue
                            if flag == 1:
                                break
                        if flag == 0:  # flag等于0表示没有满足条件的p
                            continue

                        try:
                            summary = unicode(summary).strip().encode('utf-8')  # .replace(u'\xa0', '')
                        except AttributeError:  # 没有文章的网站不存
                            continue

                        # 寻找图片
                        try:
                            image = detail_news.find(class_=self.image_class).img['src']
                        except AttributeError:  # 该新闻没有图片就不存，空格表示没有图片
                            image = ' '
                        if image == '_':
                            image = ' '

                        # 插入news表中
                        likes = 0
                        comments = 0
                        news_value = [title, self.classification, summary, image, likes, comments]
                        cur.execute('insert into news_newsmodel(Title, Classification, Summary, Image, Likes, Comments) \
                                        values (%s,%s,%s,%s,%s,%s)', news_value)

                        # 插入url表中
                        cur.execute('select * from news_newsmodel where title = %s', title)
                        news_id = cur.fetchone()
                        url_value = [self.source, urls, news_id[0]]
                        cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)', url_value)
                        conn.commit()

            cur.close()
            conn.close()

        except MySQLdb.Error, e:
            try:
                print "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error:%s" % str(e)

    def scripy_163(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
            cur = conn.cursor()
            conn.select_db('newsdb')
            cur.execute('SET NAMES utf8;')

            # 爬取网页信息
            news = self.soup.find('div', class_=self.news_class)

            # 有可能网页链接不上，只有连接上了才能爬取数据
            if news is not None:
                for link in news.find_all('a'):
                    # link = div.a
                    try:
                        if len(link.string) == 0:  # 标题为空的不要存
                            continue
                    except TypeError:
                        continue

                    # 获取标题和链接
                    title = unicode(link.string).strip().encode('utf-8')  # .replace(u'\xa0', '')  # \xa0是HTML里的&nbsp
                    urls = unicode(link.get('href')).strip().encode('utf-8')

                    # 先判断爬取到的url是否已经存到数据库中
                    cur.execute('select * from news_urlsmodel where Urls = %s', urls)
                    url_set = cur.fetchall()
                    if len(url_set) > 0:  # 说明爬取到的url已经存在了
                        continue

                    # 整合新闻
                    similar_news, similarity = merge(cur, title)
                    if similar_news is not None:  # 非空表示新闻可以整合，为空表示没有相似的新闻，直接执行后面的
                        if similarity == 1.0:  # 新闻重复了
                            cur.execute('select * from news_urlsmodel where News_id = %s', similar_news[0])
                            similar_url_set = cur.fetchall()
                            for similar_url in similar_url_set:
                                if similar_url[2] == urls:  # 如果url已经存在，那么就不存，否则存
                                    continue
                            # 如果url不存在，那么就存
                            url_value = [self.source, urls, similar_news[0]]
                            cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)',
                                        url_value)
                            print '163 multi'
                            print similar_news[1].decode('utf-8').encode('gbk', 'ignore')
                            continue
                        else:  # 整合新闻
                            print '163 make'
                            print similar_news[1].decode('utf-8').encode('gbk', 'ignore')
                            url_value = [self.source, urls, similar_news[0]]
                            cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values(%s,%s,%s)', url_value)
                            continue

                    # 根据得到的url爬取新闻的概要,如果能爬到新闻的概要才存到数据库中
                    detail_url = urls
                    try:
                        detail_html = get_html(detail_url)
                    except IOError:
                        continue

                    detail_soup = bs(detail_html, 'lxml')
                    try:
                        detail_news = detail_soup.find_all('div', class_='end-text')
                        if len(detail_news) == 0:
                            detail_news = detail_soup.find_all('div', class_='endText')
                        if len(detail_news) == 0:
                            continue
                    except AttributeError:  # 防止爬到图集，不好处理
                        continue

                    # 寻找摘要
                    flag = 0
                    for detail_div in detail_news:
                        for detail_p in detail_div.find_all('p'):
                            p = detail_p.string
                            try:
                                if len(p) >= 50:
                                    summary = p
                                    flag = 1  # flag等于1表示存在满足条件的摘要，跳出循环
                                    break
                            except TypeError:
                                continue
                        if flag == 1:
                            break
                    if flag == 0:  # flag等于0表示没有满足条件的p
                        continue

                    try:
                        summary = unicode(summary).strip().encode('utf-8')  # .replace(u'\xa0', '')
                    except AttributeError:  # 没有文章的网站不存
                        continue

                    # 寻找图片
                    if len(detail_news[0].find_all('p', class_=self.image_class)) == 0:  # 没有图片
                        image = ' '
                    else:
                        try:
                            image = detail_news[0].find_all('p', class_=self.image_class)[0].img['src']
                        except TypeError:
                            image = ' '

                    # 插入news表中
                    likes = 0
                    comments = 0
                    news_value = [title, self.classification, summary, image, likes, comments]
                    cur.execute('insert into news_newsmodel(Title, Classification, Summary, Image, Likes, Comments) \
                                    values (%s,%s,%s,%s,%s,%s)', news_value)

                    # 插入url表中
                    cur.execute('select * from news_newsmodel where title = %s', title)
                    news_id = cur.fetchone()
                    url_value = [self.source, urls, news_id[0]]
                    cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)', url_value)
                    conn.commit()

            cur.close()
            conn.close()

        except MySQLdb.Error, e:
            try:
                print "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error:%s" % str(e)

    def scripy_sohu(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
            cur = conn.cursor()
            conn.select_db('newsdb')
            cur.execute('SET NAMES utf8;')

            # 爬取网页信息
            news = self.soup.find('div', class_=self.news_class)

            # 有可能网页链接不上，只有连接上了才能爬取数据
            if news is not None:
                for link in news.find_all('a'):
                    # link = div.a
                    try:
                        if len(link.string) == 0:  # 标题为空的不要存
                            continue
                    except TypeError:
                        continue

                    # 获取标题和链接
                    title = unicode(link.string).strip().encode('utf-8')  # .replace(u'\xa0', '')  # \xa0是HTML里的&nbsp

                    if len(title) <= 14:  # 爬取的时候会出现”阅读全文》“这个东西，有点坑爹
                        continue

                    urls = unicode(link.get('href')).strip().encode('utf-8')

                    # 先判断爬取到的url是否已经存到数据库中
                    cur.execute('select * from news_urlsmodel where Urls = %s', urls)
                    url_set = cur.fetchall()
                    if len(url_set) > 0:  # 说明爬取到的url已经存在了
                        continue

                    # 整合新闻
                    similar_news, similarity = merge(cur, title)
                    if similar_news is not None:  # 非空表示新闻可以整合，为空表示没有相似的新闻，直接执行后面的
                        if similarity == 1.0:  # 新闻重复了
                            cur.execute('select * from news_urlsmodel where News_id = %s', similar_news[0])
                            similar_url_set = cur.fetchall()
                            for similar_url in similar_url_set:
                                if similar_url[2] == urls:  # 如果url已经存在，那么就不存，否则存
                                    continue
                            # 如果url不存在，那么就存
                            url_value = [self.source, urls, similar_news[0]]
                            cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)',
                                        url_value)
                            continue
                        else:  # 整合新闻
                            url_value = [self.source, urls, similar_news[0]]
                            cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values(%s,%s,%s)', url_value)
                            continue

                    # 根据得到的url爬取新闻的概要,如果能爬到新闻的概要才存到数据库中
                    detail_url = urls
                    try:
                        detail_html = get_html(detail_url)
                    except IOError:
                        continue

                    detail_soup = bs(detail_html, 'lxml')
                    try:
                        detail_news = detail_soup.find_all('div', class_='text clear')
                        if len(detail_news) == 0:
                            continue
                    except AttributeError:  # 防止爬到图集，不好处理
                        continue

                    # 寻找摘要
                    flag = 0
                    for detail_div in detail_news:
                        for detail_p in detail_div.find_all('p'):
                            p = detail_p.string
                            try:
                                if len(p) >= 50:
                                    summary = p
                                    flag = 1  # flag等于1表示存在满足条件的摘要，跳出循环
                                    break
                            except TypeError:
                                continue
                        if flag == 1:
                            break
                    if flag == 0:  # flag等于0表示没有满足条件的p
                        continue

                    try:
                        summary = unicode(summary).strip().encode('utf-8')  # .replace(u'\xa0', '')
                    except AttributeError:  # 没有文章的网站不存
                        continue

                    # 寻找图片
                    if len(detail_news[0].find_all('img')) == 0:  # 没有图片
                        image = ' '
                    else:
                        try:
                            image = detail_news[0].find_all('img')[0]['src']
                        except TypeError:
                            image = ' '

                    cur.execute('SET NAMES utf8;')
                    # 插入news表中
                    likes = 0
                    comments = 0
                    news_value = [title, self.classification, summary, image, likes, comments]
                    cur.execute('insert into news_newsmodel(Title, Classification, Summary, Image, Likes, Comments) \
                                    values (%s,%s,%s,%s,%s,%s)', news_value)

                    # 插入url表中
                    cur.execute('select * from news_newsmodel where title = %s', title)
                    news_id = cur.fetchone()
                    url_value = [self.source, urls, news_id[0]]
                    cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)', url_value)
                    conn.commit()

            cur.close()
            conn.close()

        except MySQLdb.Error, e:
            try:
                print "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error:%s" % str(e)

