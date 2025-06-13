from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .Serializer import OptionSerializer
from .models import Option
from .service import create_option, update_option, delete_option, get_options, get_option_by_id, add_item_to_option
from .models import Item

# Create your views here.
class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()


@api_view(['POST'])
def add_option(request):
    data = request.data
    try:
        description = data.get('description')
        items_ids = data.get('items', [])
        if not description or not items_ids:
            return Response({'error': 'All fields are required'}, status=400)
        if not items_ids:
            return Response({'error': 'Invalid items provided'}, status=400)
        option = create_option(description, items_ids)
        return Response({'message': 'Option creada exitosamente', 'option_id': option.id}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PUT'])
def update_option_view(request, option_id):
    data = request.data
    try:
        description = data.get('description')
        items_ids = data.get('items', [])
        
        if not description:
            description = None
        if not items_ids:
            items_ids = None
        
        items = Item.objects.filter(id__in=items_ids) if items_ids else None
        update_option(option_id, description, items)
        return Response({'message': 'Option actualizada exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_option_view(request, option_id):
    try:
        delete_option(option_id)
        return Response({'message': 'Option eliminada exitosamente'}, status=204)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
def get_options_view(request):
    try:
        options = get_options()
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_option_by_id_view(request, option_id):
    try:
        option = get_option_by_id(option_id)
        serializer = OptionSerializer(option)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PATCH'])
def add_item_to_option_view(request, option_id):
    data = request.data
    try:
        items = data.get('items', [])
        if not items:
            return Response({'error': 'Items are required'}, status=400)
        
        add_item_to_option(option_id, items)
        return Response({'message': 'Items added to option successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)