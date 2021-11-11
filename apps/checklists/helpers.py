from apps.checklists.models import ChecklistCategory, ChecklistSchedule, Checklist
from django.core.exceptions import ValidationError


def get_checklist_category(id):
    try:
        return ChecklistCategory.objects.get(id=id)
    except (ChecklistCategory.DoesNotExist, ValidationError):
        return None


def get_checklist_schedule(id):
    try:
        return ChecklistSchedule.objects.get(id=id)
    except (ChecklistCategory.DoesNotExist, ValidationError):
        return None


def get_checklist(id):
    try:
        return Checklist.objects.get(id=id)
    except (Checklist.DoesNotExist, ValidationError):
        return None


def update_checklist_done(mywedding):
    total_done = mywedding.checklist.filter(is_done=True).count()
    total_checklist = mywedding.checklist.all().count()

    mywedding.checklist_done = total_done
    mywedding.total_checklist = total_checklist
    mywedding.save()


def get_checklist_category_by_name(name, wedding):
    try:
        ChecklistCategory.objects.get(name=name, wedding=wedding)
        return True
    except ChecklistCategory.DoesNotExist:
        return None
