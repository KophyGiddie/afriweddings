from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.checklists.views import ChecklistCategoryViewSet, ChecklistScheduleViewSet, ChecklistViewSet, FilterChecklist


router = DefaultRouter()
router.register(r'checklist_category', ChecklistCategoryViewSet)
router.register(r'checklist_schedule', ChecklistScheduleViewSet)
router.register(r'checklist', ChecklistViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('filter_checklist/', FilterChecklist.as_view()),
]
