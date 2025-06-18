from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('DeliveryCertificate', views.DeliveryCertificateViewSet, basename='CrudDeliveryCertificate')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.create_delivery_certificate_view, name='create-delivery-certificate'),
    path('update/<int:id>/', views.update_delivery_certificate_view, name='update-delivery-certificate'),
    path('get/', views.get_delivery_certificates_view, name='get-delivery-certificates'),
    path('get/<int:id>/', views.get_delivery_certificate_by_id_view, name='get-delivery-certificate-by-id'),
    path('add-exhibit/<int:delivery_certificate_id>/<int:exhibit_id>/', views.add_exhibit_to_delivery_certificate_view, name='add-exhibit-to-delivery-certificate'),
]