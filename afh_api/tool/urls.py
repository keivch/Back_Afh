from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Tool', views.ToolViewSet, basename='CrudTool')

urlpatterns = [
    path('', include(router.urls)), 
    path('addtool/', views.addTool, name='anadir-herramienta'),
    path('updatetool/', views.updateTool, name='update-tool'),
    path('gettools/', views.geTools, name='get-tools'),
    path('gettool/<int:tool_id>', views.getToolById, name='get-tool-by-id'),
    path('delete/<int:tool_id>', views.deleteTool, name="delete-tool")
]