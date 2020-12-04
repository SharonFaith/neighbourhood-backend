from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password




class Hood(models.Model):
    name = models.CharField(max_length=255)
    local_area = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    # occupants = models.PositiveSmallIntegerField(null=True)
    #hood_admin = models.ForeignKey(User, on_delete=models.CASCADE)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **other_fields):
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
        
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, first_name=first_name, last_name=last_name,
                         password=password, **other_fields)
        #user.setpassword(password)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')        

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    profile_pic = CloudinaryField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=255)
    local_area = models.CharField(max_length=255, blank=True, null=True)
    city_town = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, null=True)
    date_registered = models.DateTimeField(auto_now = True)

    # For the system admin
    is_superuser = models.BooleanField(default=False)

    # For the hood admin
    is_staff = models.BooleanField(default=False)

    # For normal user, system admin, and hood admin
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hood = models.ForeignKey(Hood,on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    category_name = models.IntegerField(primary_key=True)

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    description = models.TextField(null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)



















