from django.shortcuts import render
from django.http import JsonResponse
from apps.prerequisites.models import *
from apps.checklists.models import *
import time
import json


def home(request):
    return render(request, 'index.html')


def populate_default_schedules(request):
    with open("checklist_categories.json", "r") as checklists:
        data = json.load(checklists)
        for item in data:
            try:
                DefaultChecklistCategory.objects.get(name=item["label"])
            except:
                DefaultChecklistCategory.objects.create(name=item["label"], identifier=item["value"])

    with open("checklist_schedules.json", "r") as checklists:
        data = json.load(checklists)
        for item in data:
            try:
                DefaultChecklistSchedule.objects.get(name=item["label"])
            except:
                DefaultChecklistSchedule.objects.create(name=item["label"], identifier=item["value"])

    return render(request, 'index.html')


def populate_default_checklist(request):
    start = time.time()
    with open("checklist_data.json", "r") as checklists:
        data = json.load(checklists)
        for item in data:
            mycategory = DefaultChecklistCategory.objects.get(identifier=item['category'])
            myschedule = DefaultChecklistSchedule.objects.get(identifier=item['schedule'])
            DefaultChecklist.objects.create(
                title=item["title"],
                description=item["description"],
                intent=item["intent"],
                category=mycategory,
                schedule=myschedule,
                is_essential=item["essential"],
                is_default=True,
                priority=item["id"],
                identifier=item["id"],
            )
    end = time.time()
    print('Time taken to run: ', end - start)
    return render(request, 'index.html')


def handler500(request):
    return JsonResponse({'message': 'The server encountered an unexpected error but do not worry, Our engineers have been notified and will fix it ASAP. Kindly try again later',
                         'response_code': '500'
                         }, status=500)


def handler404(request, exception):
    return JsonResponse({'detail': 'The page you are looking for took a day off.',
                         'response_code': '404'
                         }, status=404)
