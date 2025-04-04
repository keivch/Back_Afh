from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Ticket', views.TicketViewSet, basename='CrudTicket')

urlpatterns = [
    path('', include(router.urls)), 
    path('addticket/', views.addTicket, name='anadir-ticket'),
    path('tickets/', views.getTickets, name='obtener-tickets'),
    path('ticket/<int:ticket_id>', views.gtTicketById, name='obtener-ticket'),
    path('changestate/', views.changeState, name="cambiar-estado")
]