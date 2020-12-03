from django.db import models
from django.utils.translation import gettext_lazy
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password, local_area, city_town, country, **other_fields):
        if not email:
            raise ValueError('You must provide an email address ')
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('You must provide your first_name')
        if not last_name:
            raise ValueError('You must provide your last_name')
        if not password:
            raise ValueError('Password is required')
        if not local_area:
            raise ValueError('You must specify your local area')
        if not city_town:
            raise ValueError('You must specify your city/town')
        if not country:
            raise ValueError('You must specify your neighbourhood')
        
        
        email = self.normalize_email(email)

        user = self.model(email = email, username = username, first_name=first_name, last_name=last_name,
                         password=password, local_area=local_area, city_town=city_town, country=country, **other_fields)
        user.setpassword(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.serdefault('is_superuser', True)
        other_fields.serdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True')
        if other_fields.get('is_susperuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True')        

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(gettext_lazy('email address'),max_length=255, unique=True)
    #password = models.CharField()
    profile_pic = models.CloudinaryField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=255)
    local_area = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
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