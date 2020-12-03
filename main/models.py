from django.db import models
from django.contrib.auth.models import User

import datetime as dt


# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood_id = models.ForeignKey(Neighbourhood, null=True,blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    neighbourhood_id = models.ForeignKey(Neighbourhood, null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    description = models.TextField(null=True)

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)

class Category(models.Model):
    category_name = models.IntegerField(primary_key=True)










