from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
# from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, SignUpSerializer
from rest_framework import status
from .models import User
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .email.token import activation_token
import requests

def welcome(request):

   return redirect('api/users')

class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format = None):
        serializers = SignUpSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format = None):
        all_users = User.objects.all()
        serializers = UserSerializer(all_users, many = True)

        return Response(serializers.data)

    def post(self, request, view):
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
        login_token = requests.post(url='/api/auth-token/', data={'username':user.username, 'password':user.password})
        return Response(data = login_token)
    else:
        return HttpResponse('nothing found')
