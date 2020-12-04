from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, SignUpSerializer
from rest_framework import status
from .models import User
from rest_framework.permissions import AllowAny
# Create your views here.

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
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format = None):
        all_users = User.objects.all()
        serializers = UserSerializer(all_users, many = True)

        return Response(serializers.data)
  #  def post(self, request, format = None):
    #    serializers = UserSerializer(data=request.data)
     #   if serializers.is_valid():
     #       serializers.save()
     #       return Response(serializers.data, status=status.HTTP_201_CREATED)

     #   return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

#class UserDescription(APIView):
#    permission_classes = (IsAdminOrReadOnly,)

    # def get_user(self, pk):

    #     try:
    #         return User.objects.get(pk=pk)
    #         print(User.objects.get(pk=pk))
    #     except User.DoesNotExist:
    #         raise Http404()
            

    # def get(self, request, pk, format=None):
        
    #         user = self.get_user(pk)

    #         serializers = UserSerializer(user)
    #         return Response(serializers.data)
       
    # def put(self, request, pk, format=None):
    #     user = self.get_user(pk)
    #     serializers = UserSerializer(user, request.data)

    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response(serializers.data)
    #     else:
    #         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     user = self.get_user(pk)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


