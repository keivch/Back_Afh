from django.urls import path, include
from . import viewsIncome
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Tool', viewsIncome.IncomeViewSet, basename='CrudIncome')

urlpatterns = [
    path('', include(router.urls)),
    path('add/', viewsIncome.create_income_view, name="create income"),
    path('update/', viewsIncome.update_income_view, name="update income"),
    path('get/', viewsIncome.get_incomes_view, name='get incomes'),
    path('get/<int:income_id>', viewsIncome.get_income_by_id_view, name="income by id")
]
