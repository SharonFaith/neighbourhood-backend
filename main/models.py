from django.db import models
from django.utils.translation import gettext_lazy
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(gettext_lazy('email address'),max_length=255, unique=True)
    #password = models.CharField()
    #profile_pic = models.CloudinaryField()
    bio = models.TextField()
    local_area = models.CharField(max_length=255)
    city/town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
   # neighbourhood_id = models.ForeignKey()
    system_admin = models.BooleanField(default=False)
    neighbourhood_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    @property
    def is_superuser(self):
        status=self.system_admin
        return status
    @property
    def is_staff(self):
        status = self.neighbourhood_admin
        return status

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username