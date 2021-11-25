from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.weddings.serializer import (
    WeddingSerializer, WallPostSerializer, WeddingMediaSerializer, WeddingRoleSerializer
)
from utils.pagination import PageNumberPagination
from utils.utilities import get_admin_wedding, get_wedding
from dateutil.parser import parse
from apps.weddings.models import Wedding, WeddingRole, WallPost, WeddingMedia
from apps.weddings.helpers import create_guest_groups, get_role_by_name, generate_slug, create_wedding_roles, create_wedding, create_default_budget_categories
from apps.celerytasks.tasks import assign_wedding_checklists, update_guest_groups, compress_image
from django.db.models import Q


class AllWeddings(APIView):

    def get(self, request, *args, **kwargs):
        myqueryset = Wedding.objects.filter(Q(admins=request.user) | Q(author=request.user))
        serializer = WeddingSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)


class WeddingViewSet(viewsets.ModelViewSet):
    model = Wedding
    serializer_class = WeddingSerializer
    queryset = Wedding.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        myqueryset = get_wedding(request)
        if myqueryset:
            serializer = WeddingSerializer(myqueryset, context={'request': request})
            return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)
        return Response(error_response("You have not created a wedding yet", '168'), status=HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        wedding_date = request.data.get('wedding_date', None)
        expected_guests = request.data.get('expected_guests', None)
        country = request.data.get('country', None)
        currency = request.data.get('currency', 'GHS')
        city = request.data.get('city', None)
        partner_role = request.data.get('partner_role', None)
        partner_first_name = request.data.get('partner_first_name', None)
        partner_last_name = request.data.get('partner_last_name', None)

        mywedding = create_wedding(wedding_date,
                                   expected_guests,
                                   country,
                                   currency,
                                   partner_role,
                                   partner_last_name,
                                   request.user,
                                   city,
                                   partner_first_name)

        # Create Default stuff
        generate_slug(mywedding)
        create_wedding_roles(mywedding)
        create_default_budget_categories(mywedding, request)
        create_guest_groups(mywedding, request)

        myuser = request.user
        myuser.wedding_id = mywedding.id
        myuser.has_onboarded = True
        myuser.save()

        assign_wedding_checklists.delay(myuser.id, mywedding.id)

        serializer = WeddingSerializer(mywedding, context={'request': request})
        return Response(success_response('Wedding Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mywedding = self.get_object()

        if request.data.get('our_story') and request.data.get('our_story') != '':
            mywedding.our_story = request.data.get('our_story')

        if request.data.get('video_url') and request.data.get('video_url') != '':
            mywedding.video_url = request.data.get('video_url')

        if request.data.get('partner_role') and request.data.get('partner_role') != '':
            mywedding.partner_role = request.data.get('partner_role')

        if request.data.get('partner_first_name') and request.data.get('partner_first_name') != "":
            mywedding.partner_first_name = request.data.get("partner_first_name")

        if request.data.get('hashtag') and request.data.get('hashtag') != "":
            mywedding.hashtag = request.data.get("hashtag")

        if request.data.get('venue') and request.data.get('venue') != "":
            mywedding.venue = request.data.get("venue")

        if request.data.get('country') and request.data.get('country') != "":
            mywedding.country = request.data.get("country")

        if request.data.get('city') and request.data.get('city') != "":
            mywedding.country = request.data.get("country")

        if request.data.get('partner_last_name') and request.data.get('partner_last_name') != '':
            mywedding.partner_last_name = request.data.get("partner_last_name")

        if request.data.get('wedding_date') and request.data.get('wedding_date') != "":
            mywedding.wedding_date = parse(request.data.get("wedding_date"), dayfirst=True)

        if request.data.get('expected_guests') and request.data.get('expected_guests') != "":
            mywedding.expected_guests = request.data.get('expected_guests')

        if request.data.get('end_time') and request.data.get('end_time') != "":
            mywedding.end_time = request.data.get('end_time')

        if request.data.get('start_time') and request.data.get('start_time') != "":
            mywedding.start_time = request.data.get('start_time')

        if request.data.get('budget') and request.data.get('budget') != "":
            mywedding.budget = request.data.get('budget')

        if request.data.get('public_url') and request.data.get('public_url') != "":
            mywedding.public_url = request.data.get('public_url')

        if request.data.get('currency') and request.data.get('currency') != "":
            mywedding.currency = request.data.get('currency')

        if request.FILES.get('partner_picture'):
            mywedding.partner_picture = request.FILES.get('partner_picture')
            mywedding.save()

            compress_image.delay(mywedding.partner_picture)

        if request.FILES.get('couple_picture'):
            mywedding.couple_picture = request.FILES.get('couple_picture')
            mywedding.save()

            compress_image.delay(mywedding.couple_picture)

        mywedding.save()

        update_guest_groups.delay(mywedding.id)

        serializer = WeddingSerializer(mywedding, context={'request': request})
        return Response(success_response('Wedding Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='switch')
    def switch(self, request):
        wedding_id = request.data.get('wedding_id')

        mywedding = get_admin_wedding(wedding_id, request)
        if not mywedding:
            return Response(error_response("You do not have access to this wedding", '123'), status=HTTP_400_BAD_REQUEST)

        myuser = request.user
        myuser.wedding_id = mywedding.id
        myuser.save()

        serializer = WeddingSerializer(mywedding, context={'request': request})
        return Response(success_response('Wedding Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='post_to_wall')
    def post_to_wall(self, request):
        post = request.data.get('post')
        image = request.FILES.get('image', None)

        if not image or image != '':
            image = None

        mywedding = Wedding.objects.get(id=request.user.wedding_id)

        mypost = WallPost.objects.create(author=request.user,
                                         wedding=mywedding,
                                         post=post,
                                         image=image)

        serializer = WallPostSerializer(mypost, context={'request': request})
        return Response(success_response('Wedding Created Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='get_wallposts')
    def get_wallposts(self, request):
        mywedding = Wedding.objects.get(id=request.user.wedding_id)
        myqueryset = mywedding.wallpost.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = WallPostSerializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False, url_path='get_wedding_media')
    def get_wedding_media(self, request):
        mywedding = Wedding.objects.get(id=request.user.wedding_id)
        myqueryset = mywedding.media.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = WeddingMediaSerializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['post'], detail=False, url_path='add_wedding_media')
    def add_wedding_media(self, request):
        image = request.FILES.get('image')

        mywedding = Wedding.objects.get(id=request.user.wedding_id)

        mypost = WeddingMedia.objects.create(author=request.user,
                                             wedding=mywedding,
                                             image=image)

        compress_image.delay(mypost.image)

        serializer = WeddingMediaSerializer(mypost, context={'request': request})
        return Response(success_response('Wedding Media Created Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='delete_wall_post')
    def delete_wall_post(self, request):
        post_id = request.data.get('post_id')

        mypost = WallPost.objects.get(id=post_id)

        if mypost.author == request.user:
            mypost.delete()
        return Response(success_response('Post Deleted Successfully'), status=HTTP_200_OK)

    @action(methods=['delete'], detail=False, url_path='delete_wedding_media')
    def delete_wedding_media(self, request):
        media_id = request.data.get('media_id')

        mymedia = WeddingMedia.objects.get(id=media_id)

        if mymedia.author == request.user:
            mymedia.delete()

        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(error_response("Invalid Operation", '123'), status=HTTP_400_BAD_REQUEST)


class WeddingRoleViewSet(viewsets.ModelViewSet):
    model = WeddingRole
    serializer_class = WeddingRoleSerializer
    queryset = WeddingRole.objects.all().order_by('?')

    def list(self, request, *args, **kwargs):
        myqueryset = WeddingRole.objects.filter(wedding__id=request.user.wedding_id).order_by('?')
        serializer = WeddingRoleSerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        role = request.data.get('role', None)

        if not role:
            return Response(error_response("Please provide the name value", '150'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)

        existing_role = get_role_by_name(role, mywedding)

        if existing_role:
            return Response(error_response("A role with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

        mycategory = WeddingRole.objects.create(
            role=role,
            is_default=False,
            wedding=mywedding,
            created_by=request.user
        )

        serializer = WeddingRoleSerializer(mycategory, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        myrole = self.get_object()

        if request.data.get('role') and request.data.get('role') != '':
            myrole.role = request.data.get('role')

        myrole.save()

        serializer = WeddingRoleSerializer(myrole, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        myrole = self.get_object()
        if myrole.created_by == request.user:
            myrole.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)
