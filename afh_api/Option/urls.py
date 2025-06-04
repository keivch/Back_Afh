from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Option', views.OptionViewSet, basename='CrudOption')
urlpatterns = [
    path('', include(router.urls)),
    path('addoption/', views.add_option, name='anadir-option'),
    path('updateoption/<int:option_id>', views.update_option_view, name='update-option'),
    path('getoptions/', views.get_options_view, name='get-options'),
    path('getitem/<int:option_id>', views.get_option_by_id, name='get-option-by-id'),
    path('delete/<int:option_id>', views.delete_option_view, name="delete-option")
]