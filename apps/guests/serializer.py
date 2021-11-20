from rest_framework import serializers


class GuestEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    invited_guests = serializers.CharField()
    confirmed_guests = serializers.CharField()
    guests_cancelled = serializers.CharField()
    guests_pending = serializers.CharField()


class GuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='get_name')
    num_of_guests = serializers.IntegerField()


class GuestSerializer(serializers.Serializer):
    id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    num_of_guests = serializers.IntegerField()
    status = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()


class GuestInvitationSerializer(serializers.Serializer):
    id = serializers.CharField()
    event = GuestEventSerializer(many=False)
    guest = GuestSerializer(many=False)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


class ExtendedGuestGroupSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='get_name')
    num_of_guests = serializers.IntegerField()
    guests_invitations = serializers.SerializerMethodField('get_checklists')

    def guests_invitations(self, obj):
        category_id = self.context['request'].data.get('event_id')

        myusers = obj.guests_invitations.all()

        if category_id and category_id != '':
            myusers = myusers.filter(category__id=category_id)

        serializer = GuestInvitationSerializer(instance=myusers, many=True)
        return serializer.data
