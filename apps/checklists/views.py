from utils.responses import error_response, success_response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from apps.checklists.serializer import (
    ChecklistCategorySerializer, ChecklistScheduleSerializer,
    ChecklistSerializer, MasterChecklistScheduleSerializer
)
from utils.pagination import PageNumberPagination
from utils.utilities import get_wedding
from django.utils import timezone
from apps.checklists.helpers import update_checklist_done, get_checklist_category, get_checklist_schedule
from apps.checklists.models import ChecklistCategory, ChecklistSchedule, Checklist
from apps.checklists.helpers import get_checklist_category_by_name, get_checklist_schedule_by_name


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

        if not name:
            return Response(error_response("Please provide the name value", '150'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)

        existing_category = get_checklist_category_by_name(name, mywedding)

        if existing_category:
            return Response(error_response("A category with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

        mycategory = ChecklistCategory.objects.create(
                                  name=name,
                                  wedding=mywedding,
                                  created_by=request.user
                                )

        serializer = ChecklistCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mycategory = self.get_object()

        if request.data.get('name') and request.data.get('name') != '':
            mycategory.name = request.data.get('name')

        mycategory.save()

        serializer = ChecklistCategorySerializer(mycategory, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

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

        if not name:
            return Response(error_response("Please provide the name value", '155'), status=HTTP_400_BAD_REQUEST)

        if not priority:
            return Response(error_response("Please provide the priority value", '156'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)

        existing_schedule = get_checklist_schedule_by_name(name, mywedding)

        if existing_schedule:
            return Response(error_response("A Schedule with this name already exist", '139'), status=HTTP_400_BAD_REQUEST)

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
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

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
        is_essential = request.data.get('is_essential', False)

        if not title:
            return Response(error_response("Please provide title", '150'), status=HTTP_400_BAD_REQUEST)

        mywedding = get_wedding(request)
        myschedule = get_checklist_schedule(schedule_id)

        if not myschedule:
            return Response(error_response("Invalid schedule", '160'), status=HTTP_400_BAD_REQUEST)

        mycategory = get_checklist_category(category_id)

        if not mycategory:
            return Response(error_response("Invalid category", '160'), status=HTTP_400_BAD_REQUEST)

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
        return Response(success_response('Created Successfully', serializer.data), status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mychecklist = self.get_object()

        if request.data.get('title') and request.data.get('title'):
            mychecklist.title = request.data.get("title")

        if request.data.get('note') and request.data.get('note'):
            mychecklist.note = request.data.get("note")

        if request.data.get('description') and request.data.get('description'):
            mychecklist.description = request.data.get("description")

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
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='mark_as_done')
    def mark_as_done(self, request, *args, **kwargs):
        mychecklist = self.get_object()
        mychecklist.is_done = True
        mychecklist.time_done = timezone.now()
        mychecklist.save()

        mywedding = get_wedding(request)
        update_checklist_done(mywedding)

        serializer = ChecklistSerializer(mychecklist, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='mark_as_not_done')
    def mark_as_not_done(self, request, *args, **kwargs):
        mychecklist = self.get_object()
        mychecklist.is_done = False
        mychecklist.save()

        mywedding = get_wedding(request)

        update_checklist_done(mywedding)

        serializer = ChecklistSerializer(mychecklist, context={'request': request})
        return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        mychecklist = self.get_object()
        if mychecklist.created_by == request.user:
            mychecklist.delete()
        return Response(success_response('Deleted Successfully'), status=HTTP_200_OK)


class FilterChecklist(APIView):

    def post(self, request, *args, **kwargs):
        schedule_id = request.data.get('schedule_id')
        category_id = request.data.get('category_id')
        is_essential = request.data.get('is_essential', False)
        is_done = request.data.get('is_done', False)
        paginate = request.data.get('paginate', True)

        myqueryset = ChecklistSchedule.objects.prefetch_related('checklists', 'checklists__category', 'checklists__schedule').filter(wedding__id=request.user.wedding_id).order_by('priority')

        if schedule_id and schedule_id != '':
            myqueryset = myqueryset.filter(id=schedule_id)

        if category_id and category_id != '':
            mycategory = get_checklist_category(category_id)
            myqueryset = myqueryset.filter(checklists__category=mycategory)

        if is_essential and is_essential != '':
            myqueryset = myqueryset.filter(checklists__is_essential=is_essential)

        if is_done and is_done != '':
            myqueryset = myqueryset.filter(checklists__is_done=is_done)

        if paginate:
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(myqueryset, request)
            serializer = MasterChecklistScheduleSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = MasterChecklistScheduleSerializer(myqueryset, context={'request': request}, many=True)
            return Response(success_response('Updated Successfully', serializer.data), status=HTTP_200_OK)

