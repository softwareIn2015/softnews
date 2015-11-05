# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class NewsContext(models.Model):
    "新闻内容表"
    title = models.CharField(max_length = 100)
    context = models.TextField()
    classfication = models.CharField(max_length = 50)
    newstime = models.CharField(max_length = 50)