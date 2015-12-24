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


class NewsModel(models.Model):
    """
    新闻模型，摆阔新闻的标题、分类信息、摘要、图片
    """
    Title = models.CharField(max_length=100)
    Classification = models.CharField(max_length=100)
    Summary = models.CharField(max_length=1000)
    Image = models.CharField(max_length=1000)
    Likes = models.IntegerField()
    Comments = models.IntegerField()


class UrlsModel(models.Model):
    """
    链接的模型，存放了url和来源网站,对应的新闻
    """
    Source = models.CharField(max_length=1000)
    Urls = models.CharField(max_length=10000)
    News = models.ForeignKey(NewsModel)


class CommentsModel(models.Model):
    """
    评论模型，包含评论的内容，做评论的用户，评论的新闻
    """
    Text = models.TextField()
    User = models.ForeignKey(UserModel)
    News = models.ForeignKey(NewsModel)


class LikesModel(models.Model):
    """
    点赞模型，包含点赞的用户，IP，对应的新闻
    """
    User = models.ForeignKey(UserModel)
    Ip = models.CharField(max_length=100)
    News = models.ForeignKey(NewsModel)


class AdviceModel(models.Model):
    """
    用户意见模型
    """
    Username = models.CharField(max_length=40)
    Useremail = models.EmailField()
    Advice = models.TextField()