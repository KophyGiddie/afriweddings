from rest_framework import serializers
from apps.weddings.serializer import PublicWeddingSerializer


class GuestEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    invited_guests = serializers.CharField()
    confirmed_guests = serializers.CharField()
    guests_cancelled = serializers.CharField()
    pending_guests = serializers.CharField()


class GuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='get_name')
    num_of_guests = serializers.IntegerField()
    is_default = serializers.BooleanField()


class GuestSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    status = serializers.CharField()
    has_companion = serializers.BooleanField()
    companion_last_name = serializers.CharField()
    companion_first_name = serializers.CharField()
    email_invitation_sent = serializers.BooleanField()


class GuestInvitationSerializer(serializers.Serializer):
    id = serializers.CharField()
    event = GuestEventSerializer(many=False)
    guest = GuestSerializer(many=False)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    invite_sent = serializers.BooleanField()


class PublicGuestInvitationSerializer(serializers.Serializer):
    id = serializers.CharField()
    event = GuestEventSerializer(many=False)
    guest = GuestSerializer(many=False)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    invite_sent = serializers.BooleanField()
    wedding = PublicWeddingSerializer(many=False)


class ExtendedGuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='get_name')
    num_of_guests = serializers.IntegerField()
    guests_invitations = serializers.SerializerMethodField('get_guests_invitations')

    def get_guests_invitations(self, obj):
        event_id = self.context['request'].data.get('event_id')

        myusers = obj.guests_invitations.all()

        if event_id and event_id != '':
            myusers = myusers.filter(event__id=event_id)

        serializer = GuestInvitationSerializer(instance=myusers, many=True)
        return serializer.data
