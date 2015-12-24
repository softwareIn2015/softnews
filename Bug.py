# -*- coding: utf-8 -*-
# __author__ = 'Xiang'
import urllib
from bs4 import BeautifulSoup as bs
import MySQLdb


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


def show_data(cur):
    """
    查看数据库中的数据
    :param cur: 数据库操作的cursor
    :return:
    """
    cur.execute('select * from news_urlsmodel')
    urls = cur.fetchall()
    for url in urls:
        print url

    cur.execute('select * from news_newsmodel')
    news = cur.fetchall()
    for new in news:
        print new


def merge(cur, title_, classfication_):
    """
    整合新闻
    :param cur: 数据库操作的cursor
    :param title_: 需要整合的新闻的链接
    :param classfication_:需要整合的新闻的分类
    :return:
    """
    cur.execute('SET NAMES utf8;')
    cur.execute('select * from news_newsmodel where Classification = %s', classfication_)
    news_set = cur.fetchall()  # 所有和需要整合的新闻类别相同的新闻的集合
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
        self.soup = bs(self.html, 'lxml', from_encoding="utf-8")
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

            # 爬取网页信息
            news = self.soup.find('div', class_=self.news_class)

            for div in news.find_all('div'):
                for link in div.find_all('a'):
                    try:
                        if len(link.string) == 0:  # 标题为空的不要存
                            continue
                    except TypeError:
                        continue

                    # 获取标题和链接
                    title = unicode(link.string).strip().encode('utf-8')  # .replace(u'\xa0', '')  # \xa0是HTML里的&nbsp
                    urls = unicode(link.get('href')).strip().encode('utf-8')

                    # 整合新闻
                    similar_news, similarity = merge(cur, title, self.classification)
                    if similar_news is not None:  # 非空表示新闻可以整合，为空表示没有相似的新闻，直接执行后面的
                        if similarity == 1.0:  # 新闻重复了
                            continue
                        else:  # 整合新闻
                            print 'cao'
                            print similar_news[1].decode('utf-8').encode('gbk', 'ignore')
                            print 'cao'
                            url_value = [self.source, urls, similar_news]
                            cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)',
                                        url_value)
                            continue

                    # 根据得到的url爬取新闻的概要,如果能爬到新闻的概要才存到数据库中
                    detail_url = urls
                    try:
                        detail_html = get_html(detail_url)
                    except IOError:
                        continue

                    detail_soup = bs(detail_html, 'lxml', from_encoding="utf-8")
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

                    cur.execute('SET NAMES utf8;')
                    # 插入news表中
                    likes = 0
                    news_value = [title, self.classification, summary, image, likes]
                    cur.execute('insert into news_newsmodel(Title, Classification, Summary, Image, Likes) \
                                    values (%s,%s,%s,%s,%s)', news_value)

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

            # 爬取网页信息
            news = self.soup.find('div', class_=self.news_class)

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

                # 整合新闻
                similar_news, similarity = merge(cur, title, self.classification)
                if similar_news is not None:  # 非空表示新闻可以整合，为空表示没有相似的新闻，直接执行后面的
                    if similarity == 1.0:  # 新闻重复了
                        continue
                    else:  # 整合新闻
                        print 'shit'
                        print similar_news[1].decode('utf-8').encode('gbk', 'ignore')
                        print 'shit'
                        url_value = [self.source, urls, similar_news]
                        cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)', url_value)
                        continue

                # 根据得到的url爬取新闻的概要,如果能爬到新闻的概要才存到数据库中
                detail_url = urls
                try:
                    detail_html = get_html(detail_url)
                except IOError:
                    continue

                detail_soup = bs(detail_html, 'lxml', from_encoding="utf-8")
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

                cur.execute('SET NAMES utf8;')
                # 插入news表中
                likes = 0
                news_value = [title, self.classification, summary, image, likes]
                cur.execute('insert into news_newsmodel(Title, Classification, Summary, Image, Likes) \
                                values (%s,%s,%s,%s,%s)', news_value)

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

            # 爬取网页信息
            news = self.soup.find('div', class_=self.news_class)

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

                # 整合新闻
                similar_news, similarity = merge(cur, title, self.classification)
                if similar_news is not None:  # 非空表示新闻可以整合，为空表示没有相似的新闻，直接执行后面的
                    if similarity == 1.0:  # 新闻重复了
                        print "cao"
                        print similar_news[1].decode('utf-8').encode('gbk', 'ignore')
                        continue
                    else:  # 整合新闻
                        print "fuck"
                        print similar_news[1].decode('utf-8').encode('gbk', 'ignore')
                        url_value = [self.source, urls, similar_news]
                        cur.execute('insert into news_urlsmodel(Source, Urls, News_id) values (%s,%s,%s)', url_value)
                        continue

                # 根据得到的url爬取新闻的概要,如果能爬到新闻的概要才存到数据库中
                detail_url = urls
                try:
                    detail_html = get_html(detail_url)
                except IOError:
                    continue

                detail_soup = bs(detail_html, 'lxml', from_encoding="utf-8")
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
                news_value = [title, self.classification, summary, image, likes]
                cur.execute('insert into news_newsmodel(Title, Classification, Summary, Image, Likes) \
                                values (%s,%s,%s,%s,%s)', news_value)

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


if __name__ == '__main__':
    # 先将数据库中的东西删掉
    delete()

    # 新浪的信息
    news_urls_sina = ['http://news.sina.com.cn/society/', 'http://news.sina.com.cn/china/',
                      'http://news.sina.com.cn/world/', 'http://mil.news.sina.com.cn/', 'http://sports.sina.com.cn/',
                      'http://ent.sina.com.cn/', 'http://news.sina.com.cn/']  # 新闻链接
    classfications_sina = ['social', 'domestic', 'international', 'military', 'sports', 'amusement', 'hot']  # 分类
    sources_sina = ['sina', 'sina', 'sina', 'sina', 'sina', 'sina', 'sina']  # 新闻来源
    # 链接在html中div的类别
    news_class_sina = ['blk12', 'blk12', 'blk12', 'blk2 imp', 'phdnews_txt fr', 'important-news', 'p_middle']
    image_class_sina = ['img_wrapper', 'img_wrapper', 'img_wrapper', 'img_wrapper', 'img_wrapper', 'img_wrapper',
                        'img_wrapper']  # 图片在html中div的类
    for i in range(len(news_urls_sina)):
        Bugger(news_urls_sina[i], classfications_sina[i], sources_sina[i], news_class_sina[i], image_class_sina[i])

    # 网易的信息
    news_urls_163 = ['http://news.163.com/shehui/', 'http://news.163.com/domestic/', 'http://news.163.com/world/',
                     'http://war.163.com/', 'http://sports.163.com/', 'http://ent.163.com/',
                     'http://news.163.com/']  # 新闻链接
    classfications_163 = ['social', 'domestic', 'international', 'military', 'sports', 'amusement', 'hot']  # 分类
    sources_163 = ['163', '163', '163', '163', '163', '163', '163']  # 新闻来源
    # 链接在html中div的id
    news_class_163 = ['area-left', 'area-left', 'img', 'area-main', 'mod_bd', 'news_textList_top', 'ns-mr60']
    # 图片在html中div的类
    image_class_163 = ['f_center', 'f_center', 'f_center', 'f_center', 'f_center', 'f_center', 'f_center']
    for i in range(len(news_urls_163)):
        Bugger(news_urls_163[i], classfications_163[i], sources_163[i], news_class_163[i], image_class_163[i])

    # 搜狐的信息
    news_urls_sohu = ['http://news.sohu.com/shehuixinwen.shtml', 'http://news.sohu.com/guoneixinwen.shtml',
                      'http://news.sohu.com/guojixinwen.shtml', 'http://mil.sohu.com/', 'http://sports.sohu.com/',
                      'http://cul.sohu.com/culturenews/', 'http://news.sohu.com/']  # 新闻链接
    classfications_sohu = ['social', 'domestic', 'international', 'military', 'sports', 'amusement', 'hot']  # 分类
    sources_sohu = ['sohu', 'sohu', 'sohu', 'sohu', 'sohu', 'sohu', 'sohu']  # 新闻来源
    news_class_sohu = ['new-article', 'new-article', 'new-article', 'c-m-r', 'center', 'f14list', 'r']
    # 链接在html中div的class c-m-r center f14list r 万一变了就坑爹了
    image_class_sohu = ['', '', '', '', '', '', '']  # 图片在html中div的类,搜狐不用这个
    for i in range(len(news_urls_sohu)):
        Bugger(news_urls_sohu[i], classfications_sohu[i], sources_sohu[i], news_class_sohu[i], image_class_sohu[i])
