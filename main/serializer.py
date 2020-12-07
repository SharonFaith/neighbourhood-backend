from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Hood, Post, Service, Comment, Category

User = get_user_model()


class ServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        fields= '__all__'

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields= '__all__'

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields= '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, allow_null=True)
    class Meta:
        model = Post
        fields= '__all__'

class HoodSerializer(serializers.ModelSerializer):
    #users = serializers.StringRelatedField()
    hood_services = ServiceSerializer(many=True, read_only=True, allow_null=True)
    hood_posts= PostSerializer(many=True, read_only=True, allow_null=True)
    users = serializers.StringRelatedField(many=True, read_only=True, allow_null=True)
    class Meta:
        model = Hood
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
<<<<<<< HEAD
 
=======
    hood_details = HoodSerializer(source='hood', read_only=True)

>>>>>>> aac76ff4d836c04814c658733258c9cead1c4647
    class Meta:
        model = User
        exclude = ['date_registered', 'groups', 'user_permissions']

    def create(self, validated_data):
        print("VALIDATED DATA: ",validated_data)
        password = validated_data.get('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','profile_pic', 'bio', 'local_area', 'city_town', 'country', 'hood']


class JoinHoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['hood']


class ManageHoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['is_staff']