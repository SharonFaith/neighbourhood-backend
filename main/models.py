from django.db import models
from django.contrib.auth.models import User

import datetime as dt


# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    local_area = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    occupants = models.PositiveSmallIntegerField(null=True)
    neighborhood_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    category_name = models.IntegerField(primary_key=True)

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    description = models.TextField(null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)



















