from rest_framework import serializers
from apps.users.serializer import UserSerializer


class WeddingRoleSerializer(serializers.Serializer):
    role = serializers.CharField()


class WeddingSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = UserSerializer(many=False)
    partner = UserSerializer(many=False)
    hashtag = serializers.CharField()
    our_story = serializers.CharField()
    video_url = serializers.CharField()
    invited_guests = serializers.CharField()
    confirmed_guests = serializers.CharField()
    guests_cancelled = serializers.CharField()
    partner_first_name = serializers.CharField()
    currency = serializers.CharField()
    public_url = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    partner_last_name = serializers.CharField()
    venue = serializers.CharField()
    budget = serializers.DecimalField(max_digits=15, decimal_places=2)
    partner_email = serializers.CharField()
    partner_picture = serializers.URLField(source='get_partner_picture')
    couple_picture = serializers.URLField(source='get_couple_picture')
    partner_role = serializers.CharField()
    expected_guests = serializers.CharField()
    wedding_date = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
    created_at = serializers.DateTimeField()
    total_checklist = serializers.IntegerField()
    checklist_completed = serializers.IntegerField()


class WallPostSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = UserSerializer(many=False)
    post = serializers.CharField()
    image = serializers.URLField(source='get_image')


class WeddingMediaSerializer(serializers.Serializer):
    id = serializers.CharField()
    image = serializers.URLField(source='get_image')
