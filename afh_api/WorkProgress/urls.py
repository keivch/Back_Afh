from django.urls import path, include
from . import views


urlpatterns = [
    path('add/<int:work_progress_id>/<int:work_advance_id>/', views.add_work_advance_view, name='add-work-advance'),
    path('remove/<int:work_progress_id>/<int:work_advance_id>/', views.remove_work_advance_view, name='remove-work-advance'),
    path('get/<int:work_progress_id>/', views.get_work_progress_view, name='get-work-progress'),
    path('get_all/', views.get_all_work_progresses_view, name='get-all-work-progresses'),
    path('change_status/<int:work_progress_id>/', views.change_work_progress_status_view, name='change-work-progress-status'),
]