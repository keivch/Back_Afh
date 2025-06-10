from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import Item
from .Serializer import ItemSerializer
from .service import create_item, update_item, delete_item, get_items, get_item_by_id

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

@api_view(['POST'])
def add_item(request):
    data = request.data
    try:
        description = data.get('description')
        units = data.get('units')
        amount = data.get('amount')
        unit_value = data.get('unit_value')
        if not description or units is None or amount is None or unit_value is None:
            return Response({'error': 'All fields are required'}, status=400)
        item = create_item(description, units, amount, unit_value)
        return Response({'message': 'Item creado exitosamente', 'item_id': item.id}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def update_item_view(request, item_id):
    data = request.data
    try:
        description = data.get('description')
        units = data.get('units')
        amount = data.get('amount')
        unit_value = data.get('unit_value')

        if not description:
            description = None
        if units is None:
            units = None
        if amount is None:
            amount = None
        if unit_value is None:
            unit_value = None

        item = update_item(item_id, description, units, amount, unit_value)
        return Response({'message': 'Item actualizado exitosamente', 'id_item': item.id}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_item_view(request, item_id):
    try:
        delete_item(item_id)
        return Response({'message': 'Item eliminado exitosamente'}, status=204)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_items_view(request):
    try:
        items = get_items()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_item_by_id_view(request, item_id):
    try:
        item = get_item_by_id(item_id)
        if item is None:
            return Response({'error': 'Item not found'}, status=404)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)