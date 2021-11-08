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
from apps.checklists.serializer import ChecklistCategorySerializer, ChecklistScheduleSerializer, ChecklistSerializer, MasterChecklistScheduleSerializer
from utils.pagination import PageNumberPagination
from utils.utilities import get_wedding
from django.utils import timezone
from apps.checklists.helpers import update_checklist_done, get_checklist_category, get_checklist_schedule
from apps.checklists.models import ChecklistCategory, ChecklistSchedule, Checklist


class ChecklistCategoryViewSet(viewsets.ModelViewSet):
    model = ChecklistCategory
    serializer_class = ChecklistCategorySerializer
    queryset = ChecklistCategory.objects.all().order_by('?')

    def list(self, request, *args, **kwargs):
        myqueryset = ChecklistCategory.objects.filter(wedding__id=request.user.wedding_id).order_by('?')
        serializer = ChecklistCategorySerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', None)

        mywedding = get_wedding(request)

        mycategory = ChecklistCategory.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  created_by=request.user
                                )

        serializer = ChecklistCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mycategory = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mycategory.name = request.data.get('name')

        mycategory.save()

        serializer = ChecklistCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mycategory = self.get_object()
        if mycategory.created_by == request.user:
            mycategory.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class ChecklistScheduleViewSet(viewsets.ModelViewSet):
    model = ChecklistSchedule
    serializer_class = ChecklistScheduleSerializer
    queryset = ChecklistSchedule.objects.all().order_by('-priority')

    def list(self, request, *args, **kwargs):
        myqueryset = ChecklistSchedule.objects.filter(wedding__id=request.user.wedding_id).order_by('priority')
        serializer = ChecklistCategorySerializer(myqueryset, context={'request': request}, many=True)
        return Response(success_response('Data Returned Successfully', serializer.data), status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        priority = request.data.get('priority', None)

        mywedding = get_wedding(request)

        myschedule = ChecklistSchedule.objects.create(
                                  name=name,
                                  priority=priority,
                                  wedding=mywedding,
                                  created_by=request.user
                                )

        serializer = ChecklistScheduleSerializer(myschedule, context={'request': request})
        return Response(success_response('schedule Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        myschedule = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            myschedule.name = request.data.get('name')

        if request.data.get('priority') and request.data.get('priority') != '':
            myschedule.name = request.data.get('priority')

        myschedule.save()

        serializer = ChecklistScheduleSerializer(myschedule, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        myschedule = self.get_object()
        if myschedule.created_by == request.user:
            myschedule.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class ChecklistViewSet(viewsets.ModelViewSet):
    model = Checklist
    serializer_class = ChecklistSerializer
    queryset = Checklist.objects.all().order_by('priority')

    def list(self, request, *args, **kwargs):
        myqueryset = Checklist.objects.select_related('category', 'schedule').filter(wedding__id=request.user.wedding_id)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(myqueryset, request)
        serializer = self.get_serializer(result_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        title = request.data.get('title', None)
        category_id = request.data.get('category_id', None)
        schedule_id = request.data.get('schedule_id', None)
        note = request.data.get('note', None)
        is_essential = request.data.get('is_essential', None)

        mywedding = get_wedding(request)
        myschedule = get_checklist_schedule(schedule_id)
        mycategory = get_checklist_category(category_id)

        mycategory = ChecklistCategory.objects.get(id=category_id)

        mychecklist = Checklist.objects.create(
                                  title=title,
                                  wedding=mywedding,
                                  category=mycategory,
                                  schedule=myschedule,
                                  note=note,
                                  is_essential=is_essential,
                                  created_by=request.user
                                )

        update_checklist_done(mywedding)

        serializer = ChecklistSerializer(mychecklist, context={'request': request})
        return Response(success_response('Category Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mychecklist = self.get_object()

        if request.data.get('title') and request.data.get('title'):
            mychecklist.title = request.data.get("title")

        if request.data.get('note') and request.data.get('note'):
            mychecklist.note = request.data.get("note")

        if request.data.get('is_essential') and request.data.get('is_essential'):
            mychecklist.is_essential = request.data.get("is_essential")

        if request.data.get('schedule_id') and request.data.get('schedule_id'):
            myschedule = get_checklist_schedule(request.data.get('schedule_id'))
            mychecklist.schedule = myschedule

        if request.data.get('category_id') and request.data.get('category_id'):
            mycategory = get_checklist_category(request.data.get('category_id'))
            mychecklist.category = mycategory

        mychecklist.save()

        serializer = ChecklistSerializer(mychecklist, context={'request': request})
        return Response(success_response('Category Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='mark_as_done')
    def mark_as_done(self, request, *args, **kwargs):
        mychecklist = self.get_object()
        mychecklist.is_done = True
        mychecklist.save()

        mywedding = get_wedding(request)
        update_checklist_done(mywedding)

        serializer = ChecklistSerializer(mychecklist, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='mark_as_not_done')
    def mark_as_not_done(self, request, *args, **kwargs):
        mychecklist = self.get_object()
        mychecklist.is_done = True
        mychecklist.time_done = timezone.now()
        mychecklist.save()

        mywedding = get_wedding(request)

        update_checklist_done(mywedding)

        serializer = ChecklistSerializer(mychecklist, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        mycategory = self.get_object()
        if mycategory.created_by == request.user:
            mycategory.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class FilterChecklist(APIView):

    def post(self, request, *args, **kwargs):
        schedule_id = request.data.get('schedule_id')
        category_id = request.data.get('category_id')
        is_essential = request.data.get('is_essential')
        is_done = request.data.get('is_done')
        paginate = request.data.get('paginate', True)

        myqueryset = ChecklistSchedule.objects.prefetch_related('checklists', 'checklists__category').filter(wedding__id=request.user.wedding_id).order_by('priority')

        if schedule_id and schedule_id != '':
            myschedule = get_checklist_schedule(schedule_id)
            myqueryset = myqueryset.filter(schedule=myschedule)

        if category_id and category_id != '':
            myschedule = get_checklist_category(schedule_id)
            myqueryset = myqueryset.filter(schedule=myschedule)

        if is_essential and is_essential != '':
            myqueryset = myqueryset.filter(is_essential=is_essential)

        if is_done and is_done != '':
            myqueryset = myqueryset.filter(is_essential=is_essential)

        if paginate:
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(myqueryset, request)
            serializer = MasterChecklistScheduleSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = MasterChecklistScheduleSerializer(myqueryset, context={'request': request})
            return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

