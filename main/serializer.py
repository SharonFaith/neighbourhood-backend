from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Hood

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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



class HoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hood
        fields = '__all__'
