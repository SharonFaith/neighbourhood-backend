from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import welcome


urlpatterns = [
   
    #path('', welcome, name='welcome'),
    path('api/users/', views.UserList.as_view(),name='user-list'),
    path('activate-account/<uid>/<token>/', views.activate_account, name='activation_email'),
    path('api/auth/signup/', views.UserSignUp.as_view(), name='signup' ),
    path('api/auth/login/', views.UserLogin.as_view(), name='login'),
    path('api/v1/hoods/', views.HoodList.as_view(), name='hoods'),
    path('api/v1/user/', views.SingleUser.as_view(), name='single_user'),
    path('api/v1/view_hood/', views.OneHood.as_view(), name='one_hood'),
    path('api/v1/create_hood/', views.CreateHood.as_view(), name='create_hood'),
    #re_path(r'api/v1/manage_hood/(?P<pk>[0-9]+)/', views.ManageHood.as_view(), name='appoint_hood_admin'),
    path('api/v1/profile/', views.EditProfile.as_view(), name='edit profile'),
    path('api/v1/manage_hood/', views.ManageHood.as_view(), name='appoint_hood_admin'),
    #path('api/v1/edit_hood/', views.OneHood.as_view(), name='edit-hood')
    path('api/v1/all_posts/', views.PostList.as_view(), name='all_posts'),
    path('api/v1/all_comments/', views.ListComments.as_view(), name='all_comments'),
    path('api/v1/all_categories/', views.ListCategories.as_view(), name='all_categories'),
    path('api/v1/all_services/', views.ListServices.as_view(), name='all_services'),
    path('api/v1/join/', views.JoinHood.as_view(), name='join_hood'),
    #path('api/v1/post/', views.AddPost.as_view(), name='add_post'),
    path('api/v1/hood_posts/', views.HoodPosts.as_view(), name='hood_posts'),
    path('api/v1/hood_services/', views.HoodServices.as_view(), name='hood_services'),
    path('api/v1/manage_categ/', views.ManageCategs.as_view(),name='edit_categ' ),
    path('api/v1/add_comment/', views.AddComments.as_view(), name='add_comment'),
    path('api/v1/manage_service/', views.ManageService.as_view(), name='service'),
    path('api/v1/manage_user/', views.ManageUser.as_view(), name='service'),

]

