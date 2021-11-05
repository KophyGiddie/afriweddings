from apps.checklists.models import ChecklistCategory, ChecklistSchedule, Checklist


def get_checklist_category(id):
    try:
        return ChecklistCategory.objects.get(id=id)
    except ChecklistCategory.DoesNotExist:
        return None


def get_checklist_schedule(id):
    try:
        return ChecklistSchedule.objects.get(id=id)
    except ChecklistCategory.DoesNotExist:
        return None


def get_checklist(id):
    try:
        return Checklist.objects.get(id=id)
    except Checklist.DoesNotExist:
        return None


def update_checklist_done(mywedding):
    total_done = mywedding.checklist.filter(is_done=True).count()
    total_checklist = mywedding.checklist.all().count()

    mywedding.checklist_done = total_done
    mywedding.total_checklist = total_checklist
    mywedding.save()
