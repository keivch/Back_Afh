from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import Quotes
from .Serializer import QuotesSerializer
from django.http import HttpResponse
from Option.models import Option
from .service import create_quote, update_quote, delete_quote, get_quotes, get_quote_by_id, pdf_quote

# Create your views here.
class QuotesViewSet(viewsets.ModelViewSet):
    serializer_class = QuotesSerializer
    queryset = Quotes.objects.all()

@api_view(['POST'])
def add_quote(request):
    data = request.data
    try:
        description = data.get('description')
        customer_id = data.get('customer_id')
        options_ids = data.get('options', [])
        tasks = data.get('tasks', [])
        options = Option.objects.filter(id__in=options_ids)
        if not description or not customer_id or not options:
            return Response({'error': 'All fields are required'}, status=400)
        create_quote(customer_id, options, description, tasks)
        return Response({'message': 'Cotizacion creada exitosamente'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PUT'])
def update_quote_view(request, quote_id):
    data = request.data
    try:
        description = data.get('description')
        customer_id = data.get('customer_id')
        options_ids = data.get('options', [])
        tasks = data.get('tasks', [])
        
        if not description:
            description = None
        if not customer_id:
            customer_id = None
        if not options_ids:
            options_ids = None
        
        options = Option.objects.filter(id__in=options_ids) if options_ids else None
        update_quote(quote_id, customer_id, options, description, tasks)
        return Response({'message': 'Cotizacion actualizada exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_quote_view(request, quote_id):
    try:
        delete_quote(quote_id)
        return Response({'message': 'Cotizacion eliminada exitosamente'}, status=204)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_quotes_view(request):
    try:
        quotes = get_quotes()
        serializer = QuotesSerializer(quotes, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_quote_by_id_view(request, quote_id):
    try:
        quote = get_quote_by_id(quote_id)
        serializer = QuotesSerializer(quote)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def pdf_quote_view(request, id_quote):
    try:
        if not id_quote:
            return Response({'error': 'Id de la cotizacion es requerido'}, status=400)
        quote = Quotes.objects.get(id=id_quote)
        buffer = pdf_quote(id_quote)

        # Preparar respuesta como archivo descargable
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Cotizacion-{quote.code}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)