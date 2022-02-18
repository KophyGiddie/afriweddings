from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.weddings.views import (
    WeddingViewSet, AllWeddings, WeddingRoleViewSet, SearchPublicWeddings,
    WeddingFAQViewSet, WeddingScheduleEventViewSet, WeddingScheduleViewSet,
    GetPublicWedding, PublicWeddings, ValidateWeddingPublicURL, ValidateWeddingHashtag,
    FeaturedWeddings
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
    path('public_weddings/', PublicWeddings.as_view()),
    path('featured_weddings/', FeaturedWeddings.as_view()),
    path('validate_wedding_public_url/', ValidateWeddingPublicURL.as_view()),
    path('validate_wedding_hashtag/', ValidateWeddingHashtag.as_view()),
    path('get_public_wedding/', GetPublicWedding.as_view()),
    path('search_public_weddings/', SearchPublicWeddings.as_view()),
]
