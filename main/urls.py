from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import welcome


urlpatterns = [
    path('', welcome, name='welcome'),
    path('api/users/', views.UserList.as_view(),name='user-list'),
    path('activate-account/<uid>/<token>/', views.activate_account, name='activation_email'),
    path('api/auth/signup/', views.UserSignUp.as_view(), name='signup' ),
    path('api/auth/login/', views.UserLogin.as_view(), name='login'),
    path('api/v1/hoods/', views.HoodList.as_view(), name='hoods'),
    path('api/v1/user/', views.SingleUser.as_view(), name='single_user'),
    path('api/v1/view_hood/', views.OneHood.as_view(), name='one_hood'),
    path('api/v1/create_hood/', views.CreateHood.as_view(), name='create_hood'),
    #re_path(r'api/v1/manage_hood/(?P<pk>[0-9]+)/', views.ManageHood.as_view(), name='appoint_hood_admin'),
    
    path('api/v1/manage_hood/', views.ManageHood.as_view(), name='appoint_hood_admin'),
    path('api/v1/edit_hood/', views.OneHood.as_view(), name='edit-hood')
]

