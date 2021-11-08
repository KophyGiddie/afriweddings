from rest_framework import serializers


class InvitationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.CharField()
    invitation_code = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_role = serializers.CharField()
    email = serializers.CharField()
    invitation_type = serializers.CharField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
