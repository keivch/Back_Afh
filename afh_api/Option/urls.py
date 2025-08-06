from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Option', views.OptionViewSet, basename='CrudOption')
urlpatterns = [
    path('addoption/', views.add_option, name='anadir-option'),
    path('updateoption/<int:option_id>', views.update_option_view, name='update-option'),
    path('getoptions/', views.get_options_view, name='get-options'),
    path('getoption/<int:option_id>', views.get_option_by_id_view, name='get-option-by-id'),
    path('delete/<int:option_id>', views.delete_option_view, name="delete-option"),
    path('additemtooption/<int:option_id>', views.add_item_to_option_view, name='add-item-to-option'),
]