from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import welcome


urlpatterns = [
    path('', welcome, name='welcome'),
    path('api/users/', views.UserList.as_view())
]