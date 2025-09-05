from django.urls import path
from . import views

urlpatterns = [
    # Crear nuevo mantenimiento
    path('add/', views.add_maintenance_view, name='add_maintenance'),
    
    # Actualizar mantenimiento existente
    path('update/<int:maintenance_id>/', views.update_maintenance_view, name='update_maintenance'),
    
    # Obtener todos los mantenimientos
    path('get/', views.get_all_maintenances, name='get_all_maintenances'),
    
    # Obtener mantenimiento por ID
    path('get/<int:maintenance_id>/', views.get_maintenance_by_id, name='get_maintenance_by_id'),

    path('get_pdf/<int:maintenance_id>/', views.get_pdf, name='obtener_pdf')
]
