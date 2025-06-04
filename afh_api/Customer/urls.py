from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('Customer', views.CustomerViewSet, basename='CrudCustomer')

urlpatterns = [
    path('', include(router.urls)),
    path('addcustomer/', views.add_customer, name='anadir-cliente'),
    path('updatecustomer/<int:customer_id>', views.update_customer_view, name='update-customer'),
    path('getcustomers/', views.get_customers_view, name='get-customers'),
    path('getcustomer/<int:customer_id>', views.get_customer_by_id_view, name='get-customer-by-id'),
    path('delete/<int:customer_id>', views.delete_customer_view, name="delete-customer")
]