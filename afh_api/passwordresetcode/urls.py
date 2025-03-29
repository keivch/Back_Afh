from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('administrator', views.PasswordResetCodeViewSet, basename='PasswordResetCode')

urlpatterns = [
    path('', include(router.urls)), 
    path('reset/', views.reset_password, name='resetPassowrd'),
    path('validate/', views.validate_code, name='validate code'),
    path('request/', views.request_password_reset, name='request code')
]