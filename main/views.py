from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .permissions import IsSuperuser, IsActivatedOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, HoodSerializer
from rest_framework import status
from .models import User, Hood
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .email.token import activation_token
from .email.activation_email import send_activation_email
import requests
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken



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
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            send_activation_email(request, user)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username).first()

        if user is not None and user.check_password(password):
            token = get_tokens(user)
            return Response(data = token)
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
    permission_classes = (IsActivatedOrReadOnly,)

    def get(self, request):
        if request.GET.get('hood_id'):
            hood_id = request.GET.get('hood_id')
            hood = Hood.objects.filter(id = hood_id).first()
            users = hood.users.all()
            if request.user in users:
                serializer = HoodSerializer(hood)
                return Response(serializer.data)
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
        except User.DoesNotExist:
            raise Http404()

    def get(self, request):
        
            hood = self.get_hood(request)

            serializers = HoodSerializer(hood)
            return Response(serializers.data)
       
    def put(self, request):
        hood = self.get_hood(request)
        serializers = HoodSerializer(hood, request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        hood = self.get_hood(request)
        hood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def patch(self, request):
        hood = self.get_object(request)
        serializer = HoodSerializer(hood, request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)





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
        user = self.get_user(request)
        print(user)
        serializer = UserSerializer(user, request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OneHood(APIView):
    permission_classes = (IsActivatedOrReadOnly,)

    def get_hood(self, request):

        # try:
        #     return Hood.objects.get(pk=pk)
            
        # except Hood.DoesNotExist:
        #     raise Http404()
        try:
            hood_id = request.GET.get('hood_id')
                
            return Hood.objects.filter(id = hood_id).first()
        except User.DoesNotExist:
            raise Http404()

    def get(self, request):
        
        hood = self.get_hood(request)

        serializers = HoodSerializer(hood)
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
