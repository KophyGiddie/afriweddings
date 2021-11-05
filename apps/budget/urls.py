from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.budget.views import BudgetCategoryViewSet, BudgetExpenseViewSet


router = DefaultRouter()
router.register(r'budget_category', BudgetCategoryViewSet)
router.register(r'budget_expense', BudgetExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
