from django.urls import path, include
from rest_framework import routers
from . import viewsBalans



urlpatterns = [
    path('get/', viewsBalans.get_balance_view, name="obtener balance"),
    path('get_by_method_of_paymenth/<int:option>', viewsBalans.get_by_method_of_paymenth_view, name='balances por metodo de pago'),
    path('get_balans_monthly/', viewsBalans.get_balans_by_month_view, name="get balans byt month")
]