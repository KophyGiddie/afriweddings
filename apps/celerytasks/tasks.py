from celery.utils.log import get_task_logger
from afriweddings.celery import app
from apps.weddings.models import Wedding
from apps.users.models import AFUser
from apps.checklists.models import Checklist, ChecklistCategory, ChecklistSchedule

logger = get_task_logger(__name__)


@app.task()
def assign_wedding_checklists(user_id, wedding_id):
    myuser = AFUser.objects.get(id=user_id)
    mywedding = Wedding.objects.get(id=wedding_id)

    #get checklist category
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
