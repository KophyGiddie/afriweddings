from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import UserNotification


class UserAvatarSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField(source='get_avatar_full')

    class Meta:
        model = get_user_model()
        fields = ('profile_picture',)


class UserAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(max_length=500, read_only=True)
    profile_picture = serializers.URLField(source='get_avatar_full')

    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email', 'username', 'profile_picture',
                  'first_name', 'last_name', 'user_type', 'has_onboarded',
                  'phone_number', 'user_role', 'created_at', 'has_multiple_weddings',
                  'has_created_wedding', 'author_role'
                  )


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField(source='get_avatar_full')

    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email', 'username', 'profile_picture',
                  'first_name', 'last_name', 'user_type', 'has_onboarded',
                  'phone_number', 'user_role', 'created_at', 'has_multiple_weddings',
                  'has_created_wedding', 'author_role'
                  )


class LimitedUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_picture = serializers.URLField(source='get_avatar_full')
    user_role = serializers.CharField()


class UserNotificationSerializer(serializers.ModelSerializer):

    elapsed_time = serializers.CharField(source='get_elapsed_time')

    class Meta:
        model = UserNotification
        fields = ('id', 'notification_type', 'message', 'object_id', 'read',
                  'elapsed_time', 'title')
