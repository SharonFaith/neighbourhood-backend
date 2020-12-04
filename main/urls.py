from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import welcome


urlpatterns = [
    path('', welcome, name='welcome'),
    path('api/users/', views.UserList.as_view()),
    path('activate-account/<uid>/<token>/', views.activate_account, name='activation_email'),
    path('api/auth/signup/', views.UserSignUp.as_view(), name='signup' ),
    path('api/auth/login/', views.UserLogin.as_view(), name='login'),
]
