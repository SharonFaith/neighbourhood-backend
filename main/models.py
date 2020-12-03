from django.db import models
from django.contrib.auth.models import User

import datetime as dt


# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood_id = models.ForeignKey(Neighbourhood, null=True,blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)