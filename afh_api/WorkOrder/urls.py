from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('WorkOrder', views.WorkOrderViewSet, basename='CrudWorkOrder')
urlpatterns = [
    path('', include(router.urls)),
    path('workorders/', views.get_work_orders_view, name='get-work-orders'),
    path('workorder/<int:id>/', views.get_work_order_by_id_view, name='get-work-order-by-id'),
    path('pdf/<int:id_workorder>/', views.pdf_quote_view, name='pdf-quote-view'),
    path('finish/<int:id>/', views.finish_work_view, name='finish-work-view'),
]