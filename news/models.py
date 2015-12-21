# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class UserModel(models.Model):
    """
    用户模型，三个属性，分别是姓名、邮箱和密码
    """
    Name = models.CharField(max_length=40, primary_key=True)
    Email = models.EmailField()
    Password = models.CharField(max_length=20)


class UrlsModel(models.Model):
    """
    链接的模型，存放了url和来源网站
    """
    Source = models.CharField(max_length=1000)
    Urls = models.CharField(max_length=10000)


class NewsModel(models.Model):
    """
    新闻模型，摆阔新闻的标题、链接、分类信息、摘要、图片
    """
    Title = models.CharField(max_length=100)
    Url = models.ForeignKey(UrlsModel)
    Classification = models.CharField(max_length=10)
    Summary = models.CharField(max_length=1000)
    Image = models.URLField()


class CommentsModel(models.Model):
    """
    评论模型，包含评论的内容，做评论的用户，评论的新闻
    """
    Text = models.TextField()
    User = models.ForeignKey(UserModel)
    News = models.ForeignKey(NewsModel)
