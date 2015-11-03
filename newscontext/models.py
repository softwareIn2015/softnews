from django.db import models

# Create your models here.

class User(models.Model):
    "用户表"
    username = models.CharField(max_length=11)
    password = models.CharField(max_length = 20)
    
class NewsContext(models.Model):
    "新闻内容表"
    title = models.CharField(max_length = 100)
    context = models.CharField()
    classfication = models.CharField()

class Newsforpeople(models.Model):
    "用户推荐表"
    user = models.ForeignKey(User)
    recommend = models.CharField()
    
    