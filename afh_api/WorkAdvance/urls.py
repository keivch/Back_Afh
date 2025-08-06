from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('WorkAdvance', views.WorkAdvanceViewSet, basename='CRUDworkAdvance')

urlpatterns = [
    path('add/', views.add_work_advance_view, name='anadir-avance'),
    path('update/<int:work_advance_id>', views.update_work_advance_view, name='update-avance'),
    path('get/', views.get_work_advance_view, name='get-advances'),
    path('get/<int:work_advance_id>', views.get_work_advance_by_id_view, name='get-advance-by-id'),
    path('delete/<int:work_advance_id>', views.delete_work_order_view, name="delete-advance")
]