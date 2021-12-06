from rest_framework import serializers


class InvitationSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.CharField()
    invitation_code = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_role = serializers.CharField()
    picture = serializers.URLField(source='get_picture')
    user_type = serializers.CharField()
    email = serializers.CharField()
    invitation_type = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


class PublicInvitationSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_role = serializers.CharField()
    picture = serializers.URLField(source='get_picture')
