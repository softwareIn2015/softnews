# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context
from django.shortcuts import render_to_response
from models import NewsContext

def show_news(request):
    news_list = NewsContext.objects.all()
    news_context = Context({"news_list":news_list})
    return render_to_response("home.html",news_context)

def add_news(request):
    if request.POST:
        post =request.POST
        addnews=NewsContext(
            title = post['title'],
            context= post['context'],
            newstime=post['newstime'],
            classfication = post['classfication']
            )
        addnews.save()
        return render_to_response("addnews.html")
    else:
        return render_to_response("addnews.html")
def detail_news(request):
    detail_id=request.GET["id"]
    news = NewsContext.objects.get(id = detail_id)
    newsdetailContext = Context({"newsdetail":news})
    return render_to_response("detail.html",newsdetailContext)
    
def login(request):
    return render_to_response("login.html")
    
def regist(request):
    return render_to_response("regist.html")