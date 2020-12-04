from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework import status
from .models import User
# Create your views here.

def welcome(request):

   return redirect('api/users')

class UserList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format = None):
        all_users = User.objects.all()
        serializers = UserSerializer(all_users, many = True)

        return Response(serializers.data)

