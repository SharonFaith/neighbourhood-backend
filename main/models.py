from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class User():
    first_name = models.CharField(max_length=255)
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
    system_admin = models.BooleanField()
    neighbourhood_admin = models.BooleanField()
    is_active = models.BooleanField()

    @property
    def is_superuser(self):
        status=self.system_admin
        return status
    @property
    def is_staff(self):
        status = self.neighbourhood_admin
        return status