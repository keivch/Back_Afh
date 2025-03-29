from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('administrator', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),  # Esto incluirá todas las rutas generadas por el router
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
