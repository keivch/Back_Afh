from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_view, name='add_cost'),
    path('get/<int:cost_id>/', views.get_view, name='get_cost'),
    path('update/<int:cost_id>/', views.update_view, name='update_cost'),
    path('delete/<int:cost_id>/', views.delete_view, name='delete_cost'),
    path('get/', views.list_all_view, name='list_all_costs'),
    path('generate-pdf/<int:cost_id>/', views.generate_pdf_view, name='generate_pdf_cost'),
]
