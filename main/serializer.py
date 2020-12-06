from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Hood

User = get_user_model()



class HoodSerializer(serializers.ModelSerializer):
    #users = serializers.StringRelatedField()
    class Meta:
        model = Hood
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    hood_details = HoodSerializer(source='hood', read_only=True)

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
        fields = ['profile_pic', 'bio', 'local_area', 'city_town', 'country', 'hood']