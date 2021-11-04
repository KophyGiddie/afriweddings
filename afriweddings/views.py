from django.shortcuts import render
from django.http import JsonResponse
from apps.prerequisites.models import *


def home(request):
    return render(request, 'index.html')


def populate_schedules(request):
    with open("checklist_categories.json", "r") as checklists:
        data = json.load(checklists)
        for check in data:
            if not DefaultChecklistCategory.objects.filter(name=check["label"]).exist():
                DefaultChecklistCategory.objects.create(name=check["label"], identifier=check["value"])

    with open("checklist_schedules.json", "r") as checklists:
        data = json.load(checklists)
        for check in data:
            if not DefaultChecklistSchedule.objects.filter(name=check["label"]).exist():
                DefaultChecklistSchedule.objects.create(name=check["label"], identifier=check["value"])

    return render(request, 'index.html')


def populate_checklist(request):
    with open("checklist_data.json", "r") as checklists:
        data = json.load(checklists)
        for check in data:
            mycategory = DefaultChecklistCategory.objects.get(identifier=check['category'])
            myschedule = DefaultChecklistSchedule.objects.get(identifier=check['schedule'])
            DefaultChecklist.objects.create(
                title=check["title"],
                description=check["description"],
                category=mycategory,
                schedule=myschedule,
                is_essential=check["essential"],
                is_default=True,
                priority=check["id"],
                identifier=check["id"],
            )
    return render(request, 'index.html')


def handler500(request):
    return JsonResponse({'message': 'The server encountered an unexpected error but do not worry, Our engineers have been notified and will fix it ASAP. Kindly try again later',
                         'response_code': '500'
                         }, status=500)


def handler404(request, exception):
    return JsonResponse({'detail': 'The page you are looking for took a day off.',
                        'response_code':'404'
                        }, status=404)