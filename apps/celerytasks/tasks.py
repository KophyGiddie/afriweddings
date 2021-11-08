from celery.utils.log import get_task_logger
from afriweddings.celery import app
from apps.weddings.models import Wedding
from apps.users.models import AFUser
from apps.checklists.models import Checklist, ChecklistCategory, ChecklistSchedule
from apps.prerequisites.models import DefaultChecklist, DefaultChecklistSchedule
import time
from apps.checklists.helpers import update_checklist_done

logger = get_task_logger(__name__)


@app.task()
def assign_wedding_checklists(user_id, wedding_id):
    myuser = AFUser.objects.get(id=user_id)
    mywedding = Wedding.objects.get(id=wedding_id)

    mycategories = ChecklistCategory.objects.filter(created_by=myuser)
    for item in mycategories:
        item.wedding = mywedding
        item.save()

    myschedules = ChecklistSchedule.objects.filter(created_by=myuser)
    for item in myschedules:
        item.wedding = mywedding
        item.save()

    mychecklist = Checklist.objects.filter(created_by=myuser)
    for item in mychecklist:
        item.wedding = mywedding
        item.save()

    mywedding.total_checklist = mychecklist.count()
    mywedding.save()


@app.task()
def populate_wedding_checklist(schedule_identifier, author_id):
    start = time.time()
    myscheduled_checklist = DefaultChecklist.objects.select_related('category').filter(schedule__identifier=schedule_identifier)
    myauthor = AFUser.objects.get(id=author_id)
    mywedding = Wedding.objects.get(id=myauthor.wedding_id)
    myschedule = ChecklistSchedule.objects.get(identifier=schedule_identifier, created_by=myauthor)

    for item in myscheduled_checklist:
        Checklist.objects.create(
            title=item.title,
            created_by=myauthor,
            wedding=mywedding,
            description=item.description,
            category=ChecklistCategory.objects.get(identifier=item.category.identifier, created_by=myauthor),
            schedule=myschedule,
            is_essential=item.is_essential,
            is_default=True,
            priority=item.priority,
            identifier=item.identifier,
        )
    end = time.time()
    print('Time taken to run: ', end - start)
    update_checklist_done(mywedding)
