from django.urls import path
from .viewsAccount import (
    add_account_view,
    update_account_view,
    get_accounts_view,
    get_account_view,
)


urlpatterns = [
    path('get/', get_accounts_view, name='accounts-list'),
    path('create/', add_account_view, name='accounts-create'),
    path('get/<int:id_account>/', get_account_view, name='accounts-detail'),
    path('update/<int:id_account>', update_account_view, name='accounts-update'),
]


