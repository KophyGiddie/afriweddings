from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.weddings.views import (
    WeddingViewSet, AllWeddings, WeddingRoleViewSet, SearchPublicWeddings,
    WeddingFAQViewSet, WeddingScheduleEventViewSet, WeddingScheduleViewSet
)

router = DefaultRouter()
router.register(r'weddings', WeddingViewSet)
router.register(r'wedding_roles', WeddingRoleViewSet)
router.register(r'wedding_faqs', WeddingFAQViewSet)
router.register(r'wedding_schedule_events', WeddingScheduleEventViewSet)
router.register(r'wedding_schedule', WeddingScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all_weddings/', AllWeddings.as_view()),
    path('search_public_weddings/', SearchPublicWeddings.as_view()),
]
