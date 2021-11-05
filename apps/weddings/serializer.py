from rest_framework import serializers
from apps.users.serializer import UserSerializer


class WeddingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserSerializer(many=False)
    partner = UserSerializer(many=False)
    hashtag = serializers.CharField()
    partner_first_name = serializers.CharField()
    partner_last_name = serializers.CharField()
    venue = serializers.CharField()
    budget = serializers.DecimalField(max_digits=15, decimal_places=2)
    partner_email = serializers.CharField()
    partner_picture = serializers.URLField(source='get_partner_picture')
    partner_role = serializers.CharField()
    expected_guests = serializers.CharField()
    wedding_date = serializers.DateField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
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
