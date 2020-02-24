import hashlib
from random import randint

from django.db import models
from django.utils import timezone


class User(models.Model):
    """用户基本信息表"""
    # 客户端号
    no = models.IntegerField(db_index=True)
    score = models.IntegerField(db_index=True)
