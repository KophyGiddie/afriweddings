from django.shortcuts import render
from django.http import JsonResponse
from apps.prerequisites.models import *
from apps.checklists.models import *
import time


def home(request):
    return render(request, 'index.html')


def populate_default_schedules(request):
    with open("checklist_categories.json", "r") as checklists:
        data = json.load(checklists)
        for check in data:
            if not DefaultChecklistCategory.objects.filter(name=item["label"]).exist():
                DefaultChecklistCategory.objects.create(name=item["label"], identifier=item["value"])

    with open("checklist_schedules.json", "r") as checklists:
        data = json.load(checklists)
        for check in data:
            if not DefaultChecklistSchedule.objects.filter(name=item["label"]).exist():
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


def populate_wedding_checklist(request, schedule_identifier, author_id):
    start = time.time()
    myscheduled_checklist = DefaultChecklist.objects.select_related('category').filter(identifier=schedule_identifier)
    myauthor = AFUser.objects.get(id=int(author_id))
    myschedule = ChecklistSchedule.objects.get(identifier=schedule_identifier, created_by=author)

    for item in myscheduled_checklist:
        Checklist.objects.create(
            title=item.title,
            created_by=myauthor,
            description=item.description,
            category=ChecklistCategory.objects.get(identifier=item.category.identifier, created_by=author),
            schedule=myschedule,
            is_essential=item.is_essential,
            is_default=True,
            priority=item.priority,
            identifier=item.identifier,
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
                        'response_code':'404'
                        }, status=404)