"""softnews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url,patterns
from django.contrib import admin
from news.views import *
import settings

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^news/home/$', news_home),
    (r'^news/hot/$', hot_news),
    (r'^news/social/$', social_news),
    (r'^news/amusement/$', amusement_news),
    (r'^news/international/$', international_news),
    (r'^news/domestic/$', domestic_news),
    (r'^news/sports/$', sports_news),
    (r'^news/military/$', military_news),
    (r'^news/contact/$', contact_news),
    (r'^news/detail/$', detail_news),
    (r'^User/login/$', login),
    (r'^User/register/$', register),
)
