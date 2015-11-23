# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context
from django.shortcuts import render_to_response
from models import *


def homepage(request):
    return render_to_response('home.html')


def news_home(request):
    return render_to_response("home.html")


def hot_news(request):
    return render_to_response("hot.html")


def social_news(request):
    return render_to_response("social.html")


def amusement_news(request):
    return render_to_response("amusement.html")


def international_news(request):
    return render_to_response("international.html")


def domestic_news(request):
    return render_to_response("domestic.html")


def sports_news(request):
    return render_to_response("sports.html")


def military_news(request):
    return render_to_response("military.html")


def contact_news(request):
    return render_to_response("contact.html")


def detail_news(request):
    return render_to_response("detail.html")


def login(request):
    return render_to_response("login.html")


def register(request):
    return render_to_response("register.html")
