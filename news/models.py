# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class UserModel(models.Model):
    Name = models.CharField(max_length=40, primary_key=True)
    Email = models.EmailField()
    Password = models.CharField(max_length=20)


class UrlsModel(models.Model):
    Source = models.CharField(max_length=1000)
    Urls = models.CharField(max_length=10000)


class CommentsModel(models.Model):
    Text = models.TextField(verbose_name=u'评论内容')
    User = models.ForeignKey(UserModel)


class NewsModel(models.Model):
    Title = models.CharField(max_length=1000)
    Url = models.ForeignKey(UrlsModel)
    Summary = models.TextField()
    Comments = models.ForeignKey(CommentsModel)
    Classification = models.CharField(max_length=1000)
    Image = models.CharField(max_length=1000)
    Likes = models.IntegerField(verbose_name=u'点赞数', max_length=10000)


