from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Ticket', views.TicketViewSet, basename='CrudTicket')

urlpatterns = [
    path('addticket/', views.addTicket, name='añadir-ticket'),
    path('tickets/', views.getTickets, name='obtener-tickets'),
    path('ticket/<int:ticket_id>', views.gtTicketById, name='obtener-ticket'),
    path('changestate/', views.changeState, name="cambiar-estado"),
    path('getpdf/<int:ticket_id>', views.createPdfTicket, name='crear-el-pdf'),
    path('getinforme/', views.getInforme, name='get-informe')
]