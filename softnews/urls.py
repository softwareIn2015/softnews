from django.conf.urls import patterns, include, url
from news.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'softnews.views.home', name='home'),
    # url(r'^softnews/', include('softnews.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^shownews/$',show_news),
    (r'^addnews/$',add_news),
    (r'^news/detail/$',detail_news),
    (r'^User/login/$',login),
    (r'^User/register/$',regist),
)
