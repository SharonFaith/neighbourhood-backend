from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .permissions import IsSuperuser, IsActivatedOrReadOnly, IsInHood, IsAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, HoodSerializer, ProfileSerializer, JoinHoodSerializer, PostSerializer, ManageHoodSerializer
from .serializer import ServiceSerializer, CategorySerializer, CommentSerializer
from rest_framework import status
from .models import User, Hood, Post, Comment, Category, Service
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .email.token import activation_token
from .email.activation_email import send_activation_email
import requests
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
import json

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def welcome(request):

    return redirect('api/users')


class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    
    def post(self, request, format=None):
        print(request.data)
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            send_activation_email(request, user)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        #print(json.loads(request.body))
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username = username).first()

        if user is not None and user.check_password(password):
            token = get_tokens(user)
            return Response(data=token)
        return Response({'failed': 'not authorized'})

class UserList(APIView):
    permission_classes = (IsSuperuser,)

    def get(self, request, format=None):
        all_users = User.objects.all()
        serializers = UserSerializer(all_users, many=True)
        return Response(serializers.data)


class SingleUser(APIView):
    permission_classes=(IsAuthenticated,)

    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='user id to be returned',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_param_config])
    def get(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                serializer = UserSerializer(user)
                return Response(serializer.data)
            return Response(data={'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'detail':'no user id'}, status=status.HTTP_400_BAD_REQUEST)


class HoodList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        
        hoods = Hood.objects.all()
        serializers = HoodSerializer(hoods, many=True)
        return Response(serializers.data)

class CreateHood(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request):
        serializer = HoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    

    
    def get_hood(self, request):

        # try:
        #     return Hood.objects.get(pk=pk)
            
        # except Hood.DoesNotExist:
        #     raise Http404()
        try:
            hood_id = request.GET.get('hood_id')
                
            return Hood.objects.filter(id = hood_id).first()
        except Hood.DoesNotExist:
            raise Http404()
    
    hood_param_config = openapi.Parameter('hood_id', in_=openapi.IN_QUERY, description='id of the specific neighbourhood',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[hood_param_config])
    def get(self, request):
        if request.GET.get('hood_id', None):
            hood_id = request.GET.get('hood_id')
            hood = self.get_hood(request)
            print(hood)
            if hood != None:
                serializers = HoodSerializer(hood)
                print(serializers.data)
                return Response(serializers.data)
            return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
                    
           
    @swagger_auto_schema(manual_parameters=[hood_param_config])   
    def put(self, request):
        if request.GET.get('hood_id', None):
            hood = self.get_hood(request)
            if hood != None:
                serializers = HoodSerializer(hood, request.data)

                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data)
                else:
                    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(manual_parameters=[hood_param_config])   
    def delete(self, request):
        if request.GET.get('hood_id', None):
            hood = self.get_hood(request)
            if hood != None:
                hood.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(manual_parameters=[hood_param_config])   
    def patch(self, request):
        if request.GET.get('hood_id', None):
            hood = self.get_hood(request)
            if hood != None:
                serializer = HoodSerializer(hood, request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)




class ManageHood(APIView):
    permission_classes = (IsSuperuser,)

    def get_user(self, request):
        
        try:
            user_id = request.GET.get('user_id')
                
            return User.objects.filter(id = user_id).first()
        except User.DoesNotExist:
            raise Http404()
                  
    # def get(self, request):
        
    #     user = self.get_user(request)

    #     serializers = UserSerializer(user)
    #     return Response(serializers.data)
    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user to be set as hood admin',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_param_config])
    def patch(self, request):
        if request.GET.get('user_id', None):
            user = self.get_user(request)
            print(user)
            if user != None:
                serializer = ManageHoodSerializer(user, request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    serial2 = UserSerializer(user)
                    user_data = serial2.data
                    return Response(user_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)


class OneHood(APIView):
    permission_classes = (IsAuthenticated,)

    def get_hood(self, request):

        # try:
        #     return Hood.objects.get(pk=pk)
            
        # except Hood.DoesNotExist:
        #     raise Http404()
        try:
            hood_id = request.GET.get('hood_id', None)
                
            return Hood.objects.filter(id = hood_id).first()
        except Hood.DoesNotExist:
            raise Http404()

    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user',type=openapi.TYPE_INTEGER)

    hood_param_config = openapi.Parameter('hood_id', in_=openapi.IN_QUERY, description="id of that user's hood",type=openapi.TYPE_INTEGER)

    
    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def get(self, request):
        if request.GET.get('hood_id', None):
            
            
            hood = self.get_hood(request)
            
            if hood != None:
            
                if request.GET.get('user_id', None):
            
                    user_id = request.GET.get('user_id', None)
                    user = User.objects.filter(id = user_id).first()
                    print(user)
                    
            
                    if user != None:
                        serializer = UserSerializer(user)
                        if user.hood == None:
                            return Response({'detail':'unauthorized'}, status =status.HTTP_400_BAD_REQUEST)
                        elif user.hood.id == hood.id:
                            user = serializer.data

                            
                            return Response(user['hood_details'])
                        else: 
                            return Response({'status':'failed'}, status=status.HTTP_401_UNAUTHORIZED)
                        
            
                    return Response({'detail':'no user with that id'}, status =status.HTTP_400_BAD_REQUEST)
                return Response({'detail':'no user id provided'}, status =status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no hood with that id'}, status =status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status =status.HTTP_400_BAD_REQUEST)

class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self, request):
        
        try:
            user_id = request.GET.get('user_id')
                
            return User.objects.filter(id = user_id).first()
        except User.DoesNotExist:
            raise Http404()
    
    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user editing their profile',type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(manual_parameters=[user_param_config])    
    def patch(self, request):
        if request.GET.get('user_id', None):
            user = self.get_user(request)
            print(user)
            
            if user != None:
                
                serializer = ProfileSerializer(user, request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    serial2 = UserSerializer(user)
                    user_data = serial2.data
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)


class JoinHood(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self, request):
        
        try:
            user_id = request.GET.get('user_id')
                
            return User.objects.filter(id = user_id).first()
        except User.DoesNotExist:
            raise Http404()
    
    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user joining a hood',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_param_config])    
    def patch(self, request):
        if request.GET.get('user_id', None):
            user = self.get_user(request)
            user_id = request.GET.get('user_id')
           
            
            if user != None:
                #if user_id == id_user:
                    serializer = JoinHoodSerializer(user, request.data, partial=True) 
                    
                    if serializer.is_valid():
                        print(serializer.validated_data)
                    
                        serializer.save()
                        serial2 = UserSerializer(user)
                        user_data = serial2.data
                        return Response(user_data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                #return Response({'detail':'unauthorized to access to other users'}, status =status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)

           
class PostList(APIView):
    permission_classes = (IsSuperuser,)

    def get(self, request):
        
        posts = Post.objects.all()
        serializers = PostSerializer(posts, many=True)
        return Response(serializers.data)

class HoodPosts(APIView):
    permission_classes = (IsInHood,)

    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user (should be in that hood)',type=openapi.TYPE_INTEGER)
    hood_param_config = openapi.Parameter('hood_id', in_=openapi.IN_QUERY, description='id of the hood',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def get(self, request):

        hood_id = request.GET.get('hood_id', None)
        the_hood = Hood.objects.filter(id = hood_id).first()  

        posts = Post.objects.filter(hood = the_hood).all()
        serializers = PostSerializer(posts, many=True)
        return Response(serializers.data)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def post(self, request):
        hood_id = request.GET.get('hood_id', None)
        the_hood = Hood.objects.filter(id = hood_id).first()  
        info = request.data

        print(info)
        if the_hood != None:
            # hood = info.get('hood')
            # user = info.get('user')
            user_id = request.GET.get('user_id', None)
            user = User.objects.filter(id = user_id).first()
            print(user)    
            print(the_hood)   
            if user != None:
                if user.hood:
                    if user.hood.id == the_hood.id:
            
                        serializer = PostSerializer(data=request.data)
                        
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'detail':'user not in hood'}, status =status.HTTP_400_BAD_REQUEST)
                return Response({'detail':'user not in any hood'}, status =status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'unauthorized hood or user indicated'}, status =status.HTTP_400_BAD_REQUEST)
        return Response({'status':'no data'}, status =status.HTTP_400_BAD_REQUEST)

    post_param_config = openapi.Parameter('post_id', in_=openapi.IN_QUERY, description='id of the hood post to delete',type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config, post_param_config])
    def delete(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            post_id = request.GET.get('post_id')
            post = Post.objects.filter(id = post_id).first()
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                if post and user.is_superuser:
                    post.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({'detail':'no post with that id or no authorization'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)


class AddComments(APIView):
    permission_classes = (IsInHood,)

    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user (should be in that hood)',type=openapi.TYPE_INTEGER)
    hood_param_config = openapi.Parameter('hood_id', in_=openapi.IN_QUERY, description='id of the hood in which the post being commented on is in',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def post(self, request):
        hood_id = request.GET.get('hood_id', None)
        the_hood = Hood.objects.filter(id = hood_id).first()  
        info = request.data
        
        
        print(info)
        if the_hood != None:
            # hood = info.get('hood')
            # user = info.get('user')
            user_id = request.GET.get('user_id', None)
            user = User.objects.filter(id = user_id).first()
            print(user)    
            print(the_hood)   
            if user != None:
                if user.hood:
                    if user.hood.id == the_hood.id:
            
                        serializer = CommentSerializer(data=request.data)
                        
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'detail':'unauthorized hood or user indicated'}, status =status.HTTP_400_BAD_REQUEST)
                return Response({'detail':'user has no hood'}, status =status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status =status.HTTP_400_BAD_REQUEST)
        return Response({'status':'no data'}, status =status.HTTP_400_BAD_REQUEST)
       


# class AddPost(APIView):
#     permission_classes = (IsActivatedOrReadOnly,)
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AddCategory(APIView):
#     permission_classes = (AllowAny,)
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListServices(APIView):
    permission_classes = (IsSuperuser,)

    def get(self, request):
        service = Service.objects.all()
        serializers = ServiceSerializer(service, many=True)
        return Response(serializers.data)

class ManageService(APIView):
    permission_classes = (IsAdmin,)

    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user making the requests',type=openapi.TYPE_INTEGER)    
    service_param_config = openapi.Parameter('service_id', in_=openapi.IN_QUERY, description='id of the particular service',type=openapi.TYPE_INTEGER)
    hood_param_config = openapi.Parameter('hood_id', in_=openapi.IN_QUERY, description='hood id. Only pass param if user is a hood admin. The superuser does not take this param',type=openapi.TYPE_INTEGER)
    


    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def post(self, request):
        user_id = request.GET.get('user_id')                
        user = User.objects.filter(id = user_id).first()
        
        if user:
            if request.GET.get('hood_id', None):
                hood_id = request.GET.get('hood_id')
                the_hood = Hood.objects.filter(id = hood_id).first()
            
                #print(hood)
                if the_hood != None:
                    if user.hood.id == the_hood.id:
                        serializer = ServiceSerializer(data=request.data)
                    
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    elif user.is_superuser:
                        serializer = ServiceSerializer(data=request.data)
                    
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'detail': 'user not authorized'}, status=status.HTTP_400_BAD_REQUEST)
                    
                else:
                    return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
            elif user.is_superuser:
                serializer = ServiceSerializer(data=request.data)
                    
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                
            return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
        return  Response({'detail':'no user with that id or no user id provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def get(self, request):
        user_id = request.GET.get('user_id')
                
        user = User.objects.filter(id = user_id).first()
        print(user)
        print(user.is_staff)
        all_services = Service.objects.all()
        if user:
            if request.GET.get('hood_id', None):
                hood_id = request.GET.get('hood_id')
                the_hood = Hood.objects.filter(id = hood_id).first()
                hood_services = Service.objects.filter(hood = the_hood).all()
               
                #print(hood)
                if the_hood != None:
                    if user.hood:
                        print(user.hood.id)
                        print(hood_id)
                        if user.hood.id == the_hood.id:
                            serializers = ServiceSerializer(hood_services, many=True)
                            #print(serializers.data)
                            return Response(serializers.data)
                        elif user.is_superuser:
                            serializers = ServiceSerializer(all_services, many=True)
                            return Response(serializers.data)
                        else:
                            print('?')
                            return Response({'detail': 'user not authorized'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'detail':'no hood '}, status=status.HTTP_400_BAD_REQUEST)                                          
                elif user.is_superuser:
                    serializers = ServiceSerializer(all_services, many=True)
                    return Response(serializers.data)
                    
                else:
                    return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif user.is_superuser:
                serializers = ServiceSerializer(all_services, many=True)
                return Response(serializers.data)

            else:
                return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
        return  Response({'detail':'no user with that id or no user id provided'}, status=status.HTTP_400_BAD_REQUEST)                
           
    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config, service_param_config])   
    def put(self, request):
        service_id  = request.GET.get('service_id')
        service  = Service.objects.filter(id = service_id).first()
        user_id = request.GET.get('user_id')                
        user = User.objects.filter(id = user_id).first()
        if user:
            if request.GET.get('hood_id', None):
                hood_id = request.GET.get('hood_id')
                the_hood = Hood.objects.filter(id = hood_id).first()
                
                
                #print(hood)
                if the_hood != None:
                    if user.hood:
                        if user.hood.id == the_hood.id:
                            if service:
                                serializer = ServiceSerializer(service, data=request.data)
                            
                                if serializer.is_valid():
                                    serializer.save()
                                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                        
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            return Response({'detail': 'no service with that id'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'detail': 'user not authorized'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'detail':'no hood '}, status=status.HTTP_400_BAD_REQUEST)                                          
                    
                else:
                    return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)              
            elif user.is_superuser:
                if service:
                        serializer = ServiceSerializer(service, data=request.data)
                    
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': 'no service with that id'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
        return  Response({'detail':'no user with that id or no user id provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config, service_param_config])   
    def delete(self, request):
        user_id = request.GET.get('user_id')                
        user = User.objects.filter(id = user_id).first()
            
        service_id  = request.GET.get('service_id')
        service  = Service.objects.filter(id = service_id).first()
        if user:
            if request.GET.get('hood_id', None):
                hood_id = request.GET.get('hood_id')
                the_hood = Hood.objects.filter(id = hood_id).first()
                
                #print(hood)
                if the_hood != None:
                    if user.hood:
                        if user.hood.id == the_hood.id:
                            if service:
                                
                                service.delete()
                                return Response(status=status.HTTP_204_NO_CONTENT)
                            return Response({'detail': 'no service with that id'}, status=status.HTTP_400_BAD_REQUEST)
                    
                        return Response({'detail': 'user not authorized'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'detail':'no hood '}, status=status.HTTP_400_BAD_REQUEST)                                                                      
                return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)              
            elif user.is_superuser:
                if service:
                            
                    service.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response({'detail': 'no service with that id'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
        return  Response({'detail':'no user with that id or no user id provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config, service_param_config])   
    def patch(self, request):
        user_id = request.GET.get('user_id')                
        user = User.objects.filter(id = user_id).first()
        service_id  = request.GET.get('service_id')
        service  = Service.objects.filter(id = service_id).first()
        if user:
            if request.GET.get('hood_id', None):
                hood_id = request.GET.get('hood_id')
                the_hood = Hood.objects.filter(id = hood_id).first()
                
                
                #print(hood)
                if the_hood != None:
                    if user.hood:
                        if user.hood.id == the_hood.id:
                            if service:
                                serializer = ServiceSerializer(service, request.data, partial=True) 
                                if serializer.is_valid():
                                    serializer.save()
                                    return Response(serializer.data)
                                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                            return Response({'detail': 'no service with that id'}, status=status.HTTP_400_BAD_REQUEST)
                    
                        return Response({'detail': 'user not authorized'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'detail':'no hood '}, status=status.HTTP_400_BAD_REQUEST)                                          
                return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)              
            elif user.is_superuser:
                if service:
                        serializer = ServiceSerializer(service, request.data, partial=True) 
                        if serializer.is_valid():
                                serializer.save()
                                return Response(serializer.data)
                        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': 'no service with that id'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
        return  Response({'detail':'no user with that id or no user id provided'}, status=status.HTTP_400_BAD_REQUEST)

class HoodServices(APIView):

    permission_classes = (IsInHood,)

    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user (should be in that hood)',type=openapi.TYPE_INTEGER)
    hood_param_config = openapi.Parameter('hood_id', in_=openapi.IN_QUERY, description='id of the hood',type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[user_param_config, hood_param_config])
    def get(self, request):

        hood_id = request.GET.get('hood_id', None)
        the_hood = Hood.objects.filter(id = hood_id).first()  

        services = Service.objects.filter(hood = the_hood).all()
        serializers = ServiceSerializer(services, many=True)
        return Response(serializers.data)

class ManageCategs(APIView):

    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    categ_param_config = openapi.Parameter('categ_id', in_=openapi.IN_QUERY, description='id of the category',type=openapi.TYPE_INTEGER)
    

    @swagger_auto_schema(manual_parameters=[categ_param_config])
    def get(self, request):
        if request.GET.get('categ_id', None):
            categ_id = request.GET.get('categ_id')
            categ = Category.objects.filter(id = categ_id).first()
            #print(categ)
            if categ != None:
                serializers = CategorySerializer(categ)
                print(serializers.data)
                return Response(serializers.data)
            return Response({'detail':'no categ with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no categ id provided'}, status=status.HTTP_400_BAD_REQUEST)
                    
    
    @swagger_auto_schema(manual_parameters=[categ_param_config])
    def delete(self, request):
        if request.GET.get('categ_id', None):
            categ_id = request.GET.get('categ_id')
            categ = Category.objects.filter(id = categ_id).first()
            #print(categ)
            if categ != None:
                categ.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'no categ with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no categ id provided'}, status=status.HTTP_400_BAD_REQUEST)

class ManageUser(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request, format=None):
       
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    user_param_config = openapi.Parameter('user_id', in_=openapi.IN_QUERY, description='id of the user to be accessed',type=openapi.TYPE_INTEGER)
    

    @swagger_auto_schema(manual_parameters=[user_param_config])
    def get(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                serializer = UserSerializer(user)
                return Response(serializer.data)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'detail':'no user id'}, status=status.HTTP_400_BAD_REQUEST)
                    
           
    @swagger_auto_schema(manual_parameters=[user_param_config])   
    def put(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                serializers = UserSerializer(user, request.data)

                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data)
                else:
                    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                serializer = UserSerializer(user, request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)








class ListCategories(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data)

class ListComments(APIView):
    permission_classes = (IsSuperuser,)

    def get(self, request):
        comments = Comment.objects.all()
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)


def activate_account(request, uid, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        site = get_current_site(request)
        message = {'status':'ok'}
        return HttpResponse(message)

    else:
        return HttpResponse('nothing found')

