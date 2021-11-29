from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.weddings.views import WeddingViewSet, AllWeddings, WeddingRoleViewSet, SearchPublicWeddings

router = DefaultRouter()
router.register(r'weddings', WeddingViewSet)
router.register(r'wedding_roles', WeddingRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all_weddings/', AllWeddings.as_view()),
    path('search_public_weddings/', SearchPublicWeddings.as_view()),
]
