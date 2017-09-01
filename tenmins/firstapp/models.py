from django.db import models
from django.utils import timezone
from faker import Faker
import re
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    img = models.CharField(max_length=250)
    content = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createtime = models.DateField(default=timezone.now)
    editor_choice = models.BooleanField(default=False)
    CATE_CHOICE = {
        ('best','best'),
        ('hot','hot'),
    }

    cate_choice = models.CharField(choices=CATE_CHOICE,max_length=10,blank=True,null=True)
    author = models.ForeignKey(to=User,null=True,blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(null=True,blank=True,max_length=50)
    avatar = models.URLField(default='images/default.png')
    content = models.TextField(null=True,blank=True)
    createtime = models.DateTimeField(default=timezone.now)
    belong_to = models.ForeignKey(to=Article,related_name='comments',blank=True,null=True)

    def __str__(self):
        return self.name

# 创建新的评论数据结构
class Comment_New(models.Model):
    publisher = models.ForeignKey(to=User,related_name='comment_publisher', blank=True, null=True)
    belong_to = models.ForeignKey(to=Article, related_name='article_comment', blank=True, null=True)
    avatar = models.URLField(default='images/default.png')
    content = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.publisher.username


class Tickets(models.Model):
    voter = models.ForeignKey(to=User, related_name='tickers', blank=True, null=True)
    article = models.ForeignKey(to=Article, related_name='tickers', blank=True, null=True)
    VOTE_CHOICE = {
        ('like','like'),
        ('dislike','dislike'),
        ('normal','normal'),
    }
    vote = models.CharField(choices=VOTE_CHOICE,max_length=10, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

# 扩展user模型
class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='profile_image')

    belong_to = models.OneToOneField(to=User,related_name='userprofle')

    GENDER_CHOICE = {
        ('男生','男生'),
        ('女生','女生'),
    }
    gender = models.CharField(choices=GENDER_CHOICE,blank=True,null=True,max_length=100)

    nickname = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.nickname
