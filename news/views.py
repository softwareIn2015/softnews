# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from models import *


def search(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    post = request.POST
    newsInfo = post['searchInfo']
    searchNews = NewsModel.objects.filter(Title__contains=newsInfo)
    if searchNews:
      return render_to_response("search.html", locals())
    else:
        response = HttpResponse('未搜索到')
        return response


def homepage(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    hot_news = NewsModel.objects.filter(Classification='hot')
    hot = hot_news[0]#只使用热门新闻的第一个

    social_news = NewsModel.objects.filter(Classification='social')
    social = social_news[0]#只使用社会新闻的第一个

    amusement_news = NewsModel.objects.filter(Classification='amusement')
    amusement = amusement_news[0]#只使用娱乐新闻的第一个

    international_news = NewsModel.objects.filter(Classification='international')
    if len(international_news) > 6:#只保留前六个
        international_news = international_news[0:6]

    domestic_news = NewsModel.objects.filter(Classification='domestic')
    if len(domestic_news) > 6:#只保留前六个
        domestic_news = domestic_news[0:6]

    military_news = NewsModel.objects.filter(Classification='military')
    if len(military_news) > 6:#只保留前六个
        military_news = military_news[0:6]

    sports_news = NewsModel.objects.filter(Classification='sports')
    if len(sports_news) > 6:#只保留前六个
        sports_news = sports_news[0:6]
    if len(username) > 0:
        return render_to_response('home.html', locals())
    else:
        response = HttpResponseRedirect('/news/vhome/', locals())
        return response


def vhomepage(request):
    hot_news = NewsModel.objects.filter(Classification='hot')
    hot = hot_news[0]#只使用热门新闻的第一个

    social_news = NewsModel.objects.filter(Classification='social')
    social = social_news[0]#只使用社会新闻的第一个

    amusement_news = NewsModel.objects.filter(Classification='amusement')
    amusement = amusement_news[0]#只使用娱乐新闻的第一个

    international_news = NewsModel.objects.filter(Classification='international')
    if len(international_news) > 6:#只保留前六个
        international_news = international_news[0:6]

    domestic_news = NewsModel.objects.filter(Classification='domestic')
    if len(domestic_news) > 6:#只保留前六个
        domestic_news = domestic_news[0:6]

    military_news = NewsModel.objects.filter(Classification='military')
    if len(military_news) > 6:#只保留前六个
        military_news = military_news[0:6]

    sports_news = NewsModel.objects.filter(Classification='sports')
    if len(sports_news) > 6:#只保留前六个
        sports_news = sports_news[0:6]
    return render_to_response('vhome.html', locals())


def hot_page(request):
    username = request.COOKIES.get('username','')  #读取cookie
    hot_news = NewsModel.objects.filter(Classification='hot')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    most_like = hot_news[1]
    if len(username) > 0:
        return render_to_response("hot.html", locals())
    else:
        response = HttpResponseRedirect('/news/vhot/', locals())
        return response


def vhot_page(request):
    hot_news = NewsModel.objects.filter(Classification='hot')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    most_like = hot_news[1]
    return render_to_response("vhot.html", locals())


def social_page(request):
    username = request.COOKIES.get('username','')  #读取cookie
    social_news = NewsModel.objects.filter(Classification='social')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    if len(username) > 0:
        return render_to_response("social.html", locals())
    else:
        response = HttpResponseRedirect('/news/vsocial/', locals())
        return response


def vsocial_page(request):
    social_news = NewsModel.objects.filter(Classification='social')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("vsocial.html", locals())


def amusement_page(request):
    username = request.COOKIES.get('username','')  #读取cookie
    amusement_news = NewsModel.objects.filter(Classification='amusement')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    if len(username) > 0:
        return render_to_response("amusement.html", locals())
    else:
        response = HttpResponseRedirect('/news/vamusement/', locals())
        return response


def vamusement_page(request):
    amusement_news = NewsModel.objects.filter(Classification='amusement')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("vamusement.html", locals())


def international_page(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    international_news = NewsModel.objects.filter(Classification='international')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    if len(username) > 0:
        return render_to_response("international.html", locals())
    else:
        response = HttpResponseRedirect('/news/vinternational/', locals())
        return response


def vinternational_page(request):
    international_news = NewsModel.objects.filter(Classification='international')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("vinternational.html", locals())


def domestic_page(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    domestic_news = NewsModel.objects.filter(Classification='domestic')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    if len(username):
        return render_to_response("domestic.html", locals())
    else:
        response = HttpResponseRedirect('/news/vdomestic/', locals())
        return response


def vdomestic_page(request):
    domestic_news = NewsModel.objects.filter(Classification='domestic')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("vdomestic.html", locals())


def sports_page(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    sports_news = NewsModel.objects.filter(Classification='sports')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    if len(username):
        return render_to_response("sports.html", locals())
    else:
        response = HttpResponseRedirect('/news/vsports/', locals())
        return response


def vsports_page(request):
    sports_news = NewsModel.objects.filter(Classification='sports')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("vsports.html", locals())


def military_page(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    military_news = NewsModel.objects.filter(Classification='military')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    if len(username):
        return render_to_response("military.html", locals())
    else:
        response = HttpResponseRedirect('/news/vmilitary/', locals())
        return response


def vmilitary_page(request):
    military_news = NewsModel.objects.filter(Classification='military')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    hot_news = NewsModel.objects.filter(Classification='hot')
    most_like = hot_news[1]
    return render_to_response("vmilitary.html", locals())


def contact_page(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    if len(username):
        return render_to_response("contact.html", locals())
    else:
       response = HttpResponse('请先登录')
       return response


def detail_page(request):
    username = request.COOKIES.get('username', '')  #读取cookie
    title = request.GET['Title']
    news = NewsModel.objects.get(Title=title)
    if len(username):
        #新闻与评论的内外键，查询到评论内容
        comments = CommentsModel.objects.filter(News__Title=title)
        return render_to_response("detail.html", locals())
    else:
        response = HttpResponseRedirect('/news/vdetail/', locals())
        return response


def vdetail_page(request):
    title = request.GET['Title']
    news = NewsModel.objects.get(Title=title)
    return render_to_response("vdetail.html", locals())


def add_comment(request):
    comment_get = request.GET
    username = request.COOKIES.get('username', '')
    user = UserModel.objects.get(Name=username)
    title = comment_get['sendtitle']
    news = NewsModel.objects.get(Title=title)
    new_comment = CommentsModel(
        User=user,
        Text=comment_get['text'],
        News=news
    )
    new_comment.save()
    username = request.COOKIES.get('username', '')  #读取cookie
    comments = CommentsModel.objects.filter(News__Title=title)
    return render_to_response("detail.html", locals())


def register(request):
    if request.method == 'POST':
        post = request.POST
        result_regist = {"status": False, "data": ""}
        regist_Name = post['name']
        regist_Email = post['email']
        regist_Password = post['password']

        if regist_Name == "" or regist_Name.isspace():
             result_regist = {"status": False, "data": "用户名不为空"}
        else:
            if regist_Email == "" or regist_Email.isspace():
                 result_regist = {"status": False, "data": "邮箱不能为空"}
            else:
                if regist_Password == "" or regist_Password.isspace():
                    result_regist = {"status": False, "data": "密码不能为空"}
                else:
                    new_user = UserModel(
                        Name = regist_Name,
                        Email = regist_Email,
                        Password = regist_Password)
                    new_user.save()
                    result_regist = {"status": True, "data": "注册成功"}
                    return HttpResponseRedirect('/User/login/', locals())
    return render_to_response("register.html", locals())


def login(request):
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
                        #登录成功
                        result = {"status": True, "data": "登录成功"}
                        response = HttpResponseRedirect('/news/home/', locals())
                        response.set_cookie('username', Name, 3600)  #写入cookie
                        return response
                    else:
                        result = {"status": False, "data": "用户名或密码错误"}
                        response = HttpResponseRedirect('/User/login/', locals())
                        return response

    return render_to_response('login.html', locals())


def logout(request):
     response = HttpResponseRedirect('/User/login/', locals())
     response.delete_cookie('username')
     return response


