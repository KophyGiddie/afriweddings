from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_200_OK,
                                   HTTP_304_NOT_MODIFIED,
                                   HTTP_400_BAD_REQUEST, HTTP_400_BAD_REQUEST)
from apps.weddings.serializer import WeddingSerializer
from utils.pagination import PageNumberPagination
from dateutil.parser import parse
from apps.weddings.models import Wedding, WeddingRole
from apps.celerytasks.tasks import assign_wedding_checklists


class WeddingViewSet(viewsets.ModelViewSet):
    model = Wedding
    serializer_class = WeddingSerializer

    def list(self, request, *args, **kwargs):
        myqueryset = Wedding.objects.get(id=request.user.wedding_id)
        serializer = WeddingSerializer(myqueryset, context={'request': request})
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        wedding_date = request.data.get('wedding_date', None)
        expected_guests = request.data.get('expected_guests', None)
        country = request.data.get('country', None)
        city = request.data.get('city', None)
        budget = request.data.get('budget', None)
        start_time = request.data.get('start_time', None)
        end_time = request.data.get('end_time', None)
        partner_role = request.data.get('partner_role', None)
        partner_first_name = request.data.get('partner_first_name', None)
        partner_last_name = request.data.get('partner_last_name', None)

        wedding_date = parse(wedding_date, dayfirst=True)

        mywedding = Wedding.objects.create(
                                  wedding_date=wedding_date,
                                  expected_guests=expected_guests,
                                  country=country,
                                  partner_role=partner_role,
                                  partner_last_name=partner_last_name,
                                  partner_first_name=partner_first_name,
                                  start_time=start_time,
                                  end_time=end_time,
                                  budget=budget,
                                  city=city
                                )

        WeddingRole.objects.create(role='Groom', is_default=True, wedding=mywedding)
        WeddingRole.objects.create(role='Bride', is_default=True, wedding=mywedding)
        WeddingRole.objects.create(role='Other', is_default=True, wedding=mywedding)

        myuser = request.user
        myuser.wedding_id = mywedding.id
        myuser.save()

        assign_wedding_checklists.delay(myuser.id, mywedding.id)

        serializer = WeddingSerializer(mywedding, context={'request': request})
        return Response(success_response('Wedding Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mywedding = self.get_object()

        if not request.data.get('partner_role'):
            return Response(error_response("Please provide the partner role value", '124'), status=HTTP_400_BAD_REQUEST)

        if not request.data.get('partner_first_name'):
            return Response(error_response("Please provide the partner first name", '125'), status=HTTP_400_BAD_REQUEST)

        if not request.data.get('partner_last_name'):
            return Response(error_response("Please provide the partner last name", '126'), status=HTTP_400_BAD_REQUEST)

        if not request.data.get('wedding_date'):
            return Response(error_response("Please provide the wedding date value", '127'), status=HTTP_400_BAD_REQUEST)

        if not request.data.get('expected_guests'):
            return Response(error_response("Please provide the expected guests value", '128'), status=HTTP_400_BAD_REQUEST)

        mywedding.partner_role = request.data.get('partner_role')
        mywedding.partner_first_name = request.data.get("partner_first_name")
        mywedding.partner_last_name = request.data.get("partner_last_name")
        mywedding.wedding_date = parse(request.data.get("wedding_date"), dayfirst=True)
        mywedding.expected_guests = request.data.get('expected_guests')
        mywedding.save()
        return Response(success_response('Email Sent Successfully'), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(error_response("Invalid Operation", '123'), status=HTTP_400_BAD_REQUEST)
