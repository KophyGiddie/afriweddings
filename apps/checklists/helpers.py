from apps.checklists.models import ChecklistCategory, ChecklistSchedule, Checklist
from django.core.exceptions import ValidationError


def create_checklist_category(name, mywedding, myuser):
    """
    Creates a checklist category

    """
    mycategory = ChecklistCategory.objects.create(
        name=name,
        wedding=mywedding,
        created_by=myuser
    )
    return mycategory


def create_checklist_schedule(name, mywedding, priority, myuser):
    """
    Creates a checklist schedule

    """
    myschedule = ChecklistSchedule.objects.create(
        name=name,
        priority=priority,
        wedding=mywedding,
        created_by=myuser
    )
    return myschedule


def create_checklist(title, mywedding, mycategory, myschedule, note, is_essential, myuser):
    """
    Creates a checklist

    """
    mychecklist = Checklist.objects.create(
        title=title,
        wedding=mywedding,
        category=mycategory,
        schedule=myschedule,
        note=note,
        is_essential=is_essential,
        created_by=myuser
    )
    return mychecklist


def get_checklist_category(id):
    try:
        return ChecklistCategory.objects.get(id=id)
    except (ChecklistCategory.DoesNotExist, ValidationError):
        return None


def get_checklist_schedule(id):
    try:
        return ChecklistSchedule.objects.get(id=id)
    except (ChecklistSchedule.DoesNotExist, ValidationError):
        return None


def get_checklist(id):
    try:
        return Checklist.objects.get(id=id)
    except (Checklist.DoesNotExist, ValidationError):
        return None


def update_checklist_done(mywedding):
    total_done = mywedding.checklist.filter(is_done=True).count()
    print (total_done)
    total_checklist = mywedding.checklist.all().count()

    mywedding.checklist_completed = total_done
    mywedding.total_checklist = total_checklist
    mywedding.save()

    return True


def get_checklist_category_by_name(name, wedding):
    try:
        ChecklistCategory.objects.get(name=name, wedding=wedding)
        return True
    except ChecklistCategory.DoesNotExist:
        return None


def get_checklist_schedule_by_name(name, wedding):
    try:
        ChecklistSchedule.objects.get(name=name, wedding=wedding)
        return True
    except ChecklistSchedule.DoesNotExist:
        return None
