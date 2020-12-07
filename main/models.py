from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password


 

class Hood(models.Model):
    name = models.CharField(max_length=255, unique=True)
    local_area = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    @property
    def occupants(self):
        users = len(self.users.all())
        return users

    def __str__(self):
        return self.name


    def save_hood(self):
        self.save()

    def delete_hood(self):
        self.delete()

    @classmethod
    def update_hood(cls, id, update):
        cls.objects.filter(id = id).update(name = update)
        
        #to_update

    @classmethod
    def get_hood_by_id(cls, id):
        hood = cls.objects.filter(id = id)
        
        return hood

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

        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('You must provide your first_name')
        if not last_name:
            raise ValueError('You must provide your last_name')
        
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
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, null=True, related_name='users')
    date_registered = models.DateTimeField(auto_now = True)

    # For the system admin
    is_superuser = models.BooleanField(default=False)

    # For the hood admin
    is_staff = models.BooleanField(default=False)

    # For normal user, system admin, and hood admin
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    hood = models.ForeignKey(Hood,on_delete=models.CASCADE, related_name='hood_posts')
    content = models.TextField(max_length=400, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def update_post(cls, id, update):
        cls.objects.filter(id = id).update(content = update)
        
        #to_update

    @classmethod
    def get_post_by_id(cls, id):
        post = cls.objects.filter(id = id)
        
        return post


class Category(models.Model):
    name = models.CharField(max_length=255)


    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()

    @classmethod
    def update_category(cls, id, update):
        cls.objects.filter(id = id).update(name = update)
        
        #to_update

    @classmethod
    def get_categ_by_id(cls, id):
        category = cls.objects.filter(id = id)
        
        return category

# class A_Category(models.Model):
#     name = models.CharField(max_length=255)

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, related_name='hood_services')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_owned')
    email = models.EmailField(max_length=255)
    description = models.TextField(null=True)

    def save_service(self):
        self.save()

    def delete_service(self):
        self.delete()

    @classmethod
    def update_service(cls, id, update):
        cls.objects.filter(id = id).update(name = update)
        
        #to_update

    @classmethod
    def get_service_by_id(cls, id):
        service = cls.objects.filter(id = id)
        
        return service

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    posted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def update_comment(cls, id, update):
        cls.objects.filter(id = id).update(content = update)
        
        #to_update

    @classmethod
    def get_comment_by_id(cls, id):
        comment = cls.objects.filter(id = id)
        
        return comment

















