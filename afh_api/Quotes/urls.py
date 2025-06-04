from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('Quote', views.QuotesViewSet, basename='CrudQuote')

patpatterns = [
    path('', include(router.urls)),
    path('addquote/', views.add_quote, name='anadir-quote'),
    path('updatequote/<int:quote_id>', views.update_quote_view, name='update-quote'),
    path('getquotes/', views.get_quotes_view, name='get-quotes'),
    path('getquote/<int:quote_id>', views.get_quote_by_id_view, name='get-quote-by-id'),
    path('delete/<int:quote_id>', views.delete_quote_view, name="delete-quote")
]