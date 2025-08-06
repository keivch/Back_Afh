from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('Item', views.ItemViewSet, basename='CrudItem')

urlpatterns = [
    path('additem/', views.add_item, name='anadir-item'),
    path('updateitem/<int:item_id>', views.update_item_view, name='update-item'),
    path('getitems/', views.get_items_view, name='get-items'),
    path('getitem/<int:item_id>', views.get_item_by_id_view, name='get-item-by-id'),
    path('delete/<int:item_id>', views.delete_item_view, name="delete-item")
]