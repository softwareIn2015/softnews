# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from models import *


def homepage(request):
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

    return render_to_response('home.html', locals())


def hot_page(request):
    hot_news = NewsModel.objects.filter(Classification='hot')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("hot.html", locals())


def social_page(request):
    social_news = NewsModel.objects.filter(Classification='social')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("social.html", locals())


def amusement_page(request):
    amusement_news = NewsModel.objects.filter(Classification='amusement')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("amusement.html", locals())


def international_page(request):
    international_news = NewsModel.objects.filter(Classification='international')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("international.html", locals())


def domestic_page(request):
    domestic_news = NewsModel.objects.filter(Classification='domestic')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("domestic.html", locals())


def sports_page(request):
    sports_news = NewsModel.objects.filter(Classification='sports')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("sports.html", locals())


def military_page(request):
    military_news = NewsModel.objects.filter(Classification='military')
    # all_news = NewsModel.objects.all()
    # all_news = sorted(all_news, key=lambda t: t.Likes, reverse=True)
    # most_like = all_news[0]
    return render_to_response("military.html", locals())


def contact_page(request):
    return render_to_response("contact.html")


def detail_page(request):
    return render_to_response("detail.html")


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
                        result = {"status": True, "data":"登录成功"}
                        response = HttpResponseRedirect('/news/home/', locals())
                        response.set_cookie('username', Name, 3600)  #写入cookie
                        return response
                    else:
                        result = {"status": False, "data":"用户名或密码错误"}
                        return HttpResponseRedirect('/User/login/', locals())

    return render_to_response('login.html', locals())




