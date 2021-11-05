from rest_framework import serializers
from apps.user.serializer import UserSerializer


class WeddingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserSerializer(many=False)
    partner = UserSerializer(many=False)
    hashtag = serializers.CharField()
    partner_first_name = serializers.CharField()
    partner_email = serializers.CharField()
    partner_picture = serializers.URLField(source='get_partner_picture')
    user_role = serializers.CharField()
    email = serializers.CharField()
    invitation_type = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


class WallPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserSerializer(many=False)
    post = serializers.CharField()
    image = serializers.URLField(source='get_image')


class WeddingMediaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    post = serializers.CharField()
    image = serializers.URLField(source='get_image')
