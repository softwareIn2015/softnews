# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from models import *
from Bug import *


def search(request):
    """
    搜索
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    post = request.POST
    newsInfo = post['searchInfo']
    searchNews = NewsModel.objects.filter(Title__contains=newsInfo)
    if searchNews:
      return render_to_response("search.html", locals())
    else:
        response = HttpResponse('未搜索到')
        return response


def homepage(request):
    """
    主页
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie'

    hot_news = NewsModel.objects.filter(Classification='hot')
    len_hot_news = len(hot_news)
    if len_hot_news > 0:
        hot = hot_news[0]  # 只使用热门新闻的第一个

    social_news = NewsModel.objects.filter(Classification='social')
    len_social_news = len(social_news)
    if len_social_news > 0:
        social = social_news[0]  # 只使用社会新闻的第一个

    amusement_news = NewsModel.objects.filter(Classification='amusement')
    len_amusement_news = len(amusement_news)
    if len_amusement_news > 0:
        amusement = amusement_news[0]  # 只使用娱乐新闻的第一个

    international_news = NewsModel.objects.filter(Classification='international')
    len_international_news = len(international_news)
    if len_international_news > 6:  # 只保留前六个
        international_news = international_news[0:6]

    domestic_news = NewsModel.objects.filter(Classification='domestic')
    len_domestic_news = len(domestic_news)
    if len_domestic_news > 6:  # 只保留前六个
        domestic_news = domestic_news[0:6]

    military_news = NewsModel.objects.filter(Classification='military')
    len_military_news = len(military_news)
    if len_military_news > 6:  # 只保留前六个
        military_news = military_news[0:6]

    sports_news = NewsModel.objects.filter(Classification='sports')
    len_sports_news = len(sports_news)
    if len_sports_news > 6:  # 只保留前六个
        sports_news = sports_news[0:6]

    if len(username) > 0:
        return render_to_response('home.html', locals())
    else:
        response = HttpResponseRedirect('/news/vhome/', locals())
        return response


def vhomepage(request):
    """
    访客模式的主页
    :param request:
    :return:
    """
    hot_news = NewsModel.objects.filter(Classification='hot')
    len_hot_news = len(hot_news)
    if len_hot_news > 0:
        hot = hot_news[0]  # 只使用热门新闻的第一个

    social_news = NewsModel.objects.filter(Classification='social')
    len_social_news = len(social_news)
    if len_social_news > 0:
        social = social_news[0]  # 只使用社会新闻的第一个

    amusement_news = NewsModel.objects.filter(Classification='amusement')
    len_amusement_news = len(amusement_news)
    if len_amusement_news > 0:
        amusement = amusement_news[0]  # 只使用娱乐新闻的第一个

    international_news = NewsModel.objects.filter(Classification='international')
    len_international_news = len(international_news)
    if len_international_news > 6:  # 只保留前六个
        international_news = international_news[0:6]

    domestic_news = NewsModel.objects.filter(Classification='domestic')
    len_domestic_news = len(domestic_news)
    if len_domestic_news > 6:  # 只保留前六个
        domestic_news = domestic_news[0:6]

    military_news = NewsModel.objects.filter(Classification='military')
    len_military_news = len(military_news)
    if len_military_news > 6:  # 只保留前六个
        military_news = military_news[0:6]

    sports_news = NewsModel.objects.filter(Classification='sports')
    len_sports_news = len(sports_news)
    if len_sports_news > 6:  # 只保留前六个
        sports_news = sports_news[0:6]

    return render_to_response('vhome.html', locals())


def hot_page(request):
    """
    热点新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    hot_news = NewsModel.objects.filter(Classification='hot').order_by('Likes')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    len_ = len(hot_news)
    most_like = hot_news[len_ - 1]
    if len(username) > 0:
        return render_to_response("hot.html", locals())
    else:
        response = HttpResponseRedirect('/news/vhot/', locals())
        return response


def vhot_page(request):
    """
    访客模式的热点新闻
    :param request:
    :return:
    """
    hot_news = NewsModel.objects.filter(Classification='hot').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("vhot.html", locals())


def social_page(request):
    """
    社会新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    social_news = NewsModel.objects.filter(Classification='social')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='social').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username) > 0:
        return render_to_response("social.html", locals())
    else:
        response = HttpResponseRedirect('/news/vsocial/', locals())
        return response


def vsocial_page(request):
    """
    访客模式的社会新闻
    :param request:
    :return:
    """
    social_news = NewsModel.objects.filter(Classification='social')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='social').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vsocial.html", locals())


def amusement_page(request):
    """
    娱乐新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    amusement_news = NewsModel.objects.filter(Classification='amusement')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='amusement').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username) > 0:
        return render_to_response("amusement.html", locals())
    else:
        response = HttpResponseRedirect('/news/vamusement/', locals())
        return response


def vamusement_page(request):
    """
    访客模式的娱乐新闻
    :param request:
    :return:
    """
    amusement_news = NewsModel.objects.filter(Classification='amusement')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='amusement').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vamusement.html", locals())


def international_page(request):
    """
    国际新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    international_news = NewsModel.objects.filter(Classification='international')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='international').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username) > 0:
        return render_to_response("international.html", locals())
    else:
        response = HttpResponseRedirect('/news/vinternational/', locals())
        return response


def vinternational_page(request):
    """
    访客模式的国际新闻
    :param request:
    :return:
    """
    international_news = NewsModel.objects.filter(Classification='international')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='international').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vinternational.html", locals())


def domestic_page(request):
    """
    国内新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    domestic_news = NewsModel.objects.filter(Classification='domestic')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='domestic').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username):
        return render_to_response("domestic.html", locals())
    else:
        response = HttpResponseRedirect('/news/vdomestic/', locals())
        return response


def vdomestic_page(request):
    """
    访客模式的国内新闻
    :param request:
    :return:
    """
    domestic_news = NewsModel.objects.filter(Classification='domestic')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='domestic').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vdomestic.html", locals())


def sports_page(request):
    """
    体育新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    sports_news = NewsModel.objects.filter(Classification='sports')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='sports').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username):
        return render_to_response("sports.html", locals())
    else:
        response = HttpResponseRedirect('/news/vsports/', locals())
        return response


def vsports_page(request):
    """
    访客模式的体育新闻
    :param request:
    :return:
    """
    sports_news = NewsModel.objects.filter(Classification='sports')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='sports').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vsports.html", locals())


def military_page(request):
    """
    军事新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    military_news = NewsModel.objects.filter(Classification='military')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='military').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username):
        return render_to_response("military.html", locals())
    else:
        response = HttpResponseRedirect('/news/vmilitary/', locals())
        return response


def vmilitary_page(request):
    """
    访客模式的军事新闻
    :param request:
    :return:
    """
    military_news = NewsModel.objects.filter(Classification='military')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='military').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vmilitary.html", locals())


def contact_page(request):
    """
    用户反馈
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    hot_news = NewsModel.objects.filter(Classification='hot').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    if len(username):
        return render_to_response("contact.html", locals())
    else:
        response = HttpResponse('请先登录')
        return response


def submit_advice(request):
    """
    意见提交
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    user = UserModel.objects.get(Name=username)
    mail = user.Email
    advice = request.POST['advice']
    if len(username):
        newsadvice = AdviceModel(
            Username=username,
            Useremail=mail,
            Advice=advice
        )
        newsadvice.save()
    hot_news = NewsModel.objects.filter(Classification='hot').order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("contact.html", locals())


def detail_page(request):
    """
    详情页面
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie
    title = request.GET['Title']
    news = NewsModel.objects.get(Title=title)
    classfication = news.Classification
    hot_news = NewsModel.objects.filter(Classification=classfication).order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    zan_count = news.Likes
    if len(username):
        # 新闻与评论的内外键，查询到评论内容
        comments = CommentsModel.objects.filter(News__Title=title)
        urls = UrlsModel.objects.filter(News__Title=title)
        detail_urls = urls[0]
        return render_to_response("detail.html", locals())
    else:
        response = HttpResponseRedirect('/news/vdetail/', locals())
        return response


def vdetail_page(request):
    """
    访客模式的详情页面
    :param request:
    :return:
    """
    title = request.GET['Title']
    news = NewsModel.objects.get(Title=title)
    urls = UrlsModel.objects.filter(News__Title=title)
    detail_urls = urls[0]
    classfication = news.Classification
    hot_news = NewsModel.objects.filter(Classification=classfication).order_by('Likes')
    len_news = len(hot_news)
    most_like = hot_news[len_news - 1]
    return render_to_response("vdetail.html", locals())


def add_comment(request):
    """
    增加评论
    :param request:
    :return:
    """
    comment_post = request.POST
    username = request.COOKIES.get('username', '')
    user = UserModel.objects.get(Name=username)
    title = comment_post['sendtitle']
    news = NewsModel.objects.get(Title=title)
    new_comment = CommentsModel(
        User=user,
        Text=comment_post['text'],
        News=news
    )
    news.Comments += 1
    news.save()
    new_comment.save()
    zan_count = news.Likes
    username = request.COOKIES.get('username', '')  # 读取cookie
    comments = CommentsModel.objects.filter(News__Title=title)
    return render_to_response("detail.html", locals())


def add_likes(request):
    """
    点赞
    :param request:
    :return:
    """
    getlikes = request.GET
    # 获取用户ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    username = request.COOKIES.get('username', '')
    user = UserModel.objects.get(Name=username)
    title = getlikes['Title']
    news = NewsModel.objects.get(Title=title)
    news.Likes = int(getlikes['zan'])
    newlikes = LikesModel(
        User=user,
        Ip=ip,
        News=news)

    # 判断是否是同一用户、同一IP对此新闻点赞
    thislikes = LikesModel.objects.filter(News=news)
    flag = 0
    if thislikes:
        for like in thislikes:
            # 先修改成用户
            if user == like.User:
                flag = 0
                break
            else:
                flag = 1
        if flag == 1:
            newlikes.save()
            news.Likes += 1
            news.save()
    else:
        # 此新闻还没一个赞
        newlikes.save()
        news.Likes += 1
        news.save()
    zan_count = news.Likes
    # comments = CommentsModel.objects.filter(News__Title=title)
    # return render_to_response("detail.html", locals())
    return HttpResponse(str(zan_count))


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = request.POST
        result_regist = {"status": False, "data": ""}
        regist_name = post['name']
        regist_email = post['email']
        regist_password = post['password']
        user = UserModel.objects.filter(Name=regist_name)
        if user:
            result_regist = {"status": False, "data": "用户名已注册"}
        else:
            if regist_name == "" or regist_name.isspace():
                result_regist = {"status": False, "data": "用户名不为空"}
            else:
                if regist_email == "" or regist_email.isspace():
                    result_regist = {"status": False, "data": "邮箱不能为空"}
                else:
                    if regist_password == "" or regist_password.isspace():
                        result_regist = {"status": False, "data": "密码不能为空"}
                    else:
                        new_user = UserModel(
                            Name=regist_name,
                            Email=regist_email,
                            Password=regist_password)
                        new_user.save()
                        result_regist = {"status": True, "data": "注册成功"}
                        return HttpResponseRedirect('/User/login/', locals())
    return render_to_response("register.html", locals())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = request.POST
        # 用什么来验证？？这是一个问题
        if post:
            Name = post['name']
            Password = post['password']
            result = {"status": False, "data":""}
            if Name == "" or Name.isspace():
                result = {"status": False, "data": "用户名不能为空"}
            else:
                if Password == "" or Password.isspace():
                    result = {"status": False, "data": "密码不能为空"}
                else:
                    user = UserModel.objects.filter(Name=Name, Password=Password)
                    if user:
                        # 登录成功
                        result = {"status": True, "data": "登录成功"}
                        response = HttpResponseRedirect('/news/home/', locals())
                        response.set_cookie('username', Name, 3600*3)  # 写入cookie 登录时间是3个小时
                        return response
                    else:
                        result = {"status": False, "data": "用户名或密码错误"}
                        return render_to_response('login.html', locals())
    return render_to_response('login.html', locals())


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    response = HttpResponseRedirect('/User/login/', locals())
    response.delete_cookie('username')  # 删除cookie
    return response


def userinfo(request):
    """
    用户信息
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')
    user = UserModel.objects.get(Name=username)
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("userInfo.html", locals())


def scripy(request):
    """
    爬取新闻信息
    :param request:
    :return:
    """
    flag = 0
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
    flag = 1
    return render_to_response('scripy.html', locals())


def recommend(request):
    """
    给用户推荐每个类别的最热点新闻
    :param request:
    :return:
    """
    username = request.COOKIES.get('username', '')  # 读取cookie

    most_like = []

    # 热点类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='hot').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_hot = hot_news[len_news - 1]
        most_like.append(most_like_hot)

    # 社会类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='social').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_social = hot_news[len_news - 1]
        most_like.append(most_like_social)

    # 国内类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='domestic').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_domestic = hot_news[len_news - 1]
        most_like.append(most_like_domestic)

    # 国际类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='international').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_international = hot_news[len_news - 1]
        most_like.append(most_like_international)

    # 体育类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='sports').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_sports = hot_news[len_news - 1]
        most_like.append(most_like_sports)

    # 娱乐类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='amusement').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_amusement = hot_news[len_news - 1]
        most_like.append(most_like_amusement)

    # 军事类的最热新闻
    hot_news = NewsModel.objects.filter(Classification='military').order_by('Likes')
    len_news = len(hot_news)
    if len_news != 0:
        most_like_military = hot_news[len_news - 1]
        most_like.append(most_like_military)

    return render_to_response('recommend.html', locals())
