# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdviceModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Username', models.CharField(max_length=40)),
                ('Useremail', models.EmailField(max_length=254)),
                ('Advice', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CommentsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LikesModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Title', models.CharField(max_length=100)),
                ('Classification', models.CharField(max_length=100)),
                ('Summary', models.CharField(max_length=1000)),
                ('Image', models.CharField(max_length=1000)),
                ('Likes', models.IntegerField()),
                ('Comments', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UrlsModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Source', models.CharField(max_length=1000)),
                ('Urls', models.CharField(max_length=10000)),
                ('News', models.ForeignKey(to='news.NewsModel')),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('Name', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Password', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='likesmodel',
            name='News',
            field=models.ForeignKey(to='news.NewsModel'),
        ),
        migrations.AddField(
            model_name='likesmodel',
            name='User',
            field=models.ForeignKey(to='news.UserModel'),
        ),
        migrations.AddField(
            model_name='commentsmodel',
            name='News',
            field=models.ForeignKey(to='news.NewsModel'),
        ),
        migrations.AddField(
            model_name='commentsmodel',
            name='User',
            field=models.ForeignKey(to='news.UserModel'),
        ),
    ]
