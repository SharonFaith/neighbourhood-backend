from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
# from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework import status
from .models import User
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


class Hood(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        pass

    def post(self, request):
        pass

    def patch(self, request):
        pass

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
