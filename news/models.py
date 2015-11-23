# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class UserModel(models.Model):
    Name = models.CharField(max_length=40, primary_key=True)
    Email = models.EmailField()
    Password = models.CharField(max_length=20)

    def __unicode__(self):
        return self.Name


class UrlsModel(models.Model):
    Source = models.CharField(max_length=1000)
    Urls = models.CharField(max_length=10000)

    def __unicode__(self):
        return u'%s %s' % (self.Source, self.Urls)


class CommentsModel(models.Model):
    Text = models.TextField(verbose_name=u'评论内容')
    User = models.ForeignKey(UserModel)

    def __unicode__(self):
        return self.Text


class NewsModel(models.Model):
    Title = models.CharField(max_length=1000)
    Url = models.ForeignKey(UrlsModel)
    Summary = models.TextField()
    Comments = models.ForeignKey(CommentsModel)

    def __unicode__(self):
        return self.Title
