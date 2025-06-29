from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Exhibit', views.ExhibitViewSet, basename='CrudExhibit')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.add_exhibit_view, name='create-exhibit'),
    path('update/<int:id>/', views.update_exhibit_view, name='update-exhibit'),
    path('get/', views.get_exhibits_view, name='get-exhibits'),
    path('get/<int:id>/', views.get_exhibit_by_id_view, name='get-exhibit-by-id'),
    path('delete/<int:id>/', views.delete_exhibit_view, name='delete-exhibit'),
]