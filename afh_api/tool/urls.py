from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Tool', views.ToolViewSet, basename='CrudTool')

urlpatterns = [
    path('', include(router.urls)), 
    path('addtool/', views.addTool, name='anadir-herramienta'),
]