from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .permissions import IsSuperuser, IsActivatedOrReadOnly, IsHoodUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, HoodSerializer, ProfileSerializer, JoinHoodSerializer, PostSerializer, ManageHoodSerializer
from rest_framework import status
from .models import User, Hood, Post
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .email.token import activation_token
from .email.activation_email import send_activation_email
import requests
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
import json


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
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        all_users = User.objects.all()
        serializers = UserSerializer(all_users, many=True)
        return Response(serializers.data)

class SingleUser(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        if request.GET.get('user_id', None):
            user_id = request.GET.get('user_id')
            
            user = User.objects.filter(id = user_id).first()
            if user is not None:
                serializer = UserSerializer(user)
                return Response(serializer.data)
        return Response(data={'status':'failed'}, status=status.HTTP_400_BAD_REQUEST)


class HoodList(APIView):
    permission_classes = (AllowAny,)

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
    def delete(self, request):
        if request.GET.get('hood_id', None):
            hood = self.get_hood(request)
            if hood != None:
                hood.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
    
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

    def get(self, request):
        
            hood = self.get_hood(request)
            print(hood.id)

            
            
            user_id = request.GET.get('user_id')
            user = User.objects.filter(id = user_id).first()
            print(user)
            serializer = UserSerializer(user)
            
            if user != None:
                if user.hood == None:
                    return Response({'detail':'unauthorized'}, status =status.HTTP_400_BAD_REQUEST)
                elif user.hood.id == hood.id:
                    user = serializer.data

                    
                    return Response(user['hood_details'])
                else: 
                    return Response({'status':'failed'}, status=status.HTTP_401_UNAUTHORIZED)
                
            
            return Response({'status':'failed'}, status =status.HTTP_400_BAD_REQUEST)

class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user(self, request):
        
        try:
            user_id = request.GET.get('user_id')
                
            return User.objects.filter(id = user_id).first()
        except User.DoesNotExist:
            raise Http404()
    
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
                    return Response(user_data, status=status.HTTP_201_CREATED)
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
    
    def patch(self, request):
        if request.GET.get('user_id', None):
            user = self.get_user(request)
            print(user)
            
            if user != None:
               
                serializer = JoinHoodSerializer(user, request.data, partial=True) 
                if serializer.is_valid():
                    serializer.save()
                    serial2 = UserSerializer(user)
                    user_data = serial2.data
                    return Response(user_data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no user with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no user id provided'}, status=status.HTTP_400_BAD_REQUEST)

           
class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        
        posts = Post.objects.all()
        serializers = PostSerializer(posts, many=True)
        return Response(serializers.data)


class AddPost(APIView):
    permission_classes = (IsActivatedOrReadOnly,)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






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

