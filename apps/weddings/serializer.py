from rest_framework import serializers
from apps.users.serializer import LimitedUserSerializer


class PublicWeddingSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = LimitedUserSerializer(many=False)
    partner = LimitedUserSerializer(many=False)
    hashtag = serializers.CharField()
    schedule = serializers.CharField()
    our_story = serializers.CharField()
    video_url = serializers.CharField()
    partner_first_name = serializers.CharField()
    public_url = serializers.CharField()
    partner_last_name = serializers.CharField()
    venue = serializers.CharField()
    partner_picture = serializers.URLField(source='get_partner_picture')
    couple_picture = serializers.URLField(source='get_couple_picture')
    wedding_date = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
    is_public = serializers.BooleanField()


class WeddingRoleSerializer(serializers.Serializer):
    role = serializers.CharField()


class WeddingSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = LimitedUserSerializer(many=False)
    partner = LimitedUserSerializer(many=False)
    hashtag = serializers.CharField()
    schedule = serializers.CharField()
    our_story = serializers.CharField()
    video_url = serializers.CharField()
    invited_guests = serializers.CharField()
    confirmed_guests = serializers.CharField()
    guests_cancelled = serializers.CharField()
    pending_guests = serializers.CharField()
    partner_first_name = serializers.CharField()
    currency = serializers.CharField()
    public_url = serializers.CharField()
    is_public = serializers.BooleanField()
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
    is_admin = serializers.SerializerMethodField('get_admin_status')
    user_role_on_wedding = serializers.SerializerMethodField('get_wedding_role')

    def get_admin_status(self, obj):
        myusers = obj.admins.all()
        myuser = self.context['request'].user
        if myuser in myusers:
            return True
        else:
            return False

    def get_wedding_role(self, obj):
        print (obj.wedding_user_role.all())
        print (self.context['request'].user.id)
        myrole = obj.wedding_user_role.filter(user__id=self.context['request'].user.id)
        print (myrole)
        if myrole:
            return myrole[0].role
        return ""


class WallPostSerializer(serializers.Serializer):
    id = serializers.CharField()
    author = LimitedUserSerializer(many=False)
    post = serializers.CharField()
    image = serializers.URLField(source='get_image')


class WeddingMediaSerializer(serializers.Serializer):
    id = serializers.CharField()
    image = serializers.URLField(source='get_image')


class WeddingFAQSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
    answer = serializers.CharField()


class WeddingScheduleEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    venue = serializers.CharField()
    date = serializers.CharField()


class WeddingScheduleSerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.CharField()
    activity = serializers.CharField()


class ExtendedWeddingScheduleEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    venue = serializers.CharField()
    date = serializers.CharField()
    wedding_schedule = WeddingScheduleSerializer(many=True)
