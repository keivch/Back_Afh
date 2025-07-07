from django.urls import path, include
from . import viewsEgress
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Tool', viewsEgress.EgressViewSet, basename='CrudEgress')

urlpatterns = [
    path('', include(router.urls)), 
    path('add/', viewsEgress.create_egrees_view, name="add egress"),
    path('update/<int:egress_id>', viewsEgress.update_egress_view, name="update egress"),
    path('get/', viewsEgress.get_eggress_view, name="get egress"),
    path('get/<int:egress_id>', viewsEgress.get_egress_by_id_view, name="get egress by id")
 ]