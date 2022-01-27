from celery.utils.log import get_task_logger
from afriweddings.celery import app
from apps.weddings.models import Wedding
from utils.compress import start_compressing
from utils.utilities import send_online_invitation_email
from apps.users.models import AFUser
from apps.guests.models import GuestGroup
from apps.guests.helpers import get_guests_by_group_id
from apps.checklists.models import Checklist, ChecklistCategory, ChecklistSchedule
from apps.prerequisites.models import DefaultChecklist
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

    update_checklist_done(mywedding)


@app.task()
def populate_wedding_checklist(schedule_identifier, author_id):
    start = time.time()
    myscheduled_checklist = DefaultChecklist.objects.select_related('category').filter(schedule__identifier=schedule_identifier)
    myauthor = AFUser.objects.get(id=author_id)
    myschedule = ChecklistSchedule.objects.get(identifier=schedule_identifier, created_by=myauthor)

    for item in myscheduled_checklist:
        Checklist.objects.create(
            title=item.title,
            created_by=myauthor,
            description=item.description,
            intent=item.intent,
            category=ChecklistCategory.objects.get(identifier=item.category.identifier, created_by=myauthor),
            schedule=myschedule,
            is_essential=item.is_essential,
            is_default=True,
            priority=item.priority,
            identifier=item.identifier,
        )
    end = time.time()
    print('Time taken to run: ', end - start)


@app.task()
def update_guest_groups(mywedding_id):
    mywedding = Wedding.objects.get(id=mywedding_id)
    mygroups = GuestGroup.objects.filter(is_default=True, wedding=mywedding)

    for mygroup in mygroups:
        mygroup.wedding_creator_name = mywedding.author.first_name
        mygroup.wedding_partner_name = mywedding.partner_first_name
        mygroup.save()


@app.task()
def compress_image(image_path):
    start_compressing(image_path)


@app.task()
def send_group_invitation_task(group_id, wedding_id, invited_by, wedding_date):
    mywedding = Wedding.objects.get(id=wedding_id)
    myguests = get_guests_by_group_id(group_id, wedding_id)
    print (myguests)
    for item in myguests:
        if item.email:
            send_online_invitation_email(item.id, item.first_name, mywedding.author.first_name, wedding_date, mywedding.partner_first_name, item.email)
            item.email_invitation_sent = True
            item.save()

            guests_invitations = item.guests_invitations.all()
            for element in guests_invitations:
                element.status = 'PENDING'
                element.save()

