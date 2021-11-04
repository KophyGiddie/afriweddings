from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserAvatarSerializer(serializers.ModelSerializer):
    user_avatar = serializers.URLField(source='get_avatar_full')

    class Meta:
        model = get_user_model()
        fields = ('user_avatar',)


class UserAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(max_length=500, read_only=True)
    user_avatar = serializers.URLField(source='get_avatar_full')

    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email', 'username', 'user_avatar',
                  'first_name', 'last_name', 'user_type', 'has_onboarded',
                  'phone_number', 'user_role', 'created_at',
                  )


class UserSerializer(serializers.ModelSerializer):
    user_avatar = serializers.URLField(source='get_avatar_full')
    full_name = serializers.URLField(source='get_full_name')

    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email', 'username', 'user_avatar',
                  'first_name', 'last_name', 'user_type', 'has_onboarded',
                  'phone_number', 'user_role', 'created_at'
                  )

