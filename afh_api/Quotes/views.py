from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Quotes
from .Serializer import QuotesSerializer
from django.http import HttpResponse
from Option.models import Option
from .service import create_quote, update_quote, delete_quote, get_quotes, get_quote_by_id, pdf_quote, change_state_quote, get_quotes_whitouth_order

# Create your views here.
class QuotesViewSet(viewsets.ModelViewSet):
    serializer_class = QuotesSerializer
    queryset = Quotes.objects.all()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_quote(request):
    data = request.data
    try:
        description = data.get('description')
        customer_id = data.get('customer_id')
        options_id = data.get('options')
        tasks = data.get('tasks', [])
        iva = data.get('iva')
        utility = data.get('utility')
        unforeseen = data.get('unforeseen')
        administration = data.get('administration')
        method_of_payment = data.get('method_of_payment')
        construction = data.get('construction')

        if not description or customer_id is None or options_id is None or not tasks:
            return Response({'error': 'All fields are required'}, status=400)

        if not iva:
            iva = 0.19

        create_quote(customer_id, options_id, description, tasks, iva, utility, unforeseen, administration, method_of_payment, construction)
        return Response({'message': 'Cotización creada exitosamente'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quote_view(request, quote_id):
    data = request.data
    print(data)
    try:
        description = data.get('description')
        customer_id = data.get('customer_id')
        tasks = data.get('tasks', [])
        utility = data.get('utility')
        unforeseen = data.get('unforeseen')
        administration = data.get('administration')
        method_of_payment = data.get('method_of_payment')
        construction = data.get('construction')
        
        update_quote(
        id=quote_id,
        customer_id=customer_id,
        description=description,
        tasks=tasks,
        utility=utility,
        unforeseen=unforeseen,
        administration=administration,
        method_of_payment=method_of_payment,
        construction=construction)
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
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_state_quote_view(request, quote_id):
    data = request.data
    try:
        new_state = data.get('state')
        if new_state is None:
            return Response({'error': 'El estado es requerido'}, status=400)
        change_state_quote(quote_id, new_state)
        return Response({'message': 'Estado de la cotizacion actualizado exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_quote_whitout_order_view(request):
    try:
        quotes = get_quotes_whitouth_order()
        serializer = QuotesSerializer(quotes, many=True)
        return Response(serializer.data)
    except Exception as e:  
        return Response({'error': str(e)}, status=500)
