from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Exhibit
from .Serializer import ExhibitSerializer
from .Service import create_exhibit, update_exhibit, get_exhibits, get_exhibit_by_id

# Create your views here.
class ExhibitViewSet(viewsets.ModelViewSet):
    serializer_class = ExhibitSerializer
    queryset = Exhibit.objects.all()

@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_exhibit_view(request):
    try:
        data = request.data
        tittle = data.get('tittle')
        images = request.FILES.getlist('images')

        if not tittle:
            return Response({'error': 'El título es requerido'}, status=400)
        
        exhibit = create_exhibit(tittle, images)

        return Response({'message': 'Exhibit created successfully', 'exhibit_id': exhibit.id}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, JSONParser])
def update_exhibit_view(request, id):
    try:
        data = request.data
        tittle = data.get('title')
        image = request.FILES.getlist('image')
        if not tittle and not image:
            return Response({'error': 'Debe proporcionar al menos un título o una imagen'}, status=400)
        updated_exhibit = update_exhibit(id, tittle, image)
        if updated_exhibit:
            return Response({'message': 'Exhibit updated successfully',  'exhibit_id': updated_exhibit.id}, status=200)
        else:
            return Response({'error': 'Exhibit not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_exhibits_view(request):
    try:
        exhibits = get_exhibits()
        serializer = ExhibitSerializer(exhibits, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_exhibit_by_id_view(request, id):
    try:
        exhibit = get_exhibit_by_id(id)
        if exhibit:
            serializer = ExhibitSerializer(exhibit)
            return Response(serializer.data)
        else:
            return Response({'error': 'Exhibit not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_exhibit_view(request, id):
    try:
        exhibit = Exhibit.objects.get(id=id)
        exhibit.delete()
        return Response({'message': 'Exhibit deleted successfully'}, status=204)
    except Exhibit.DoesNotExist:
        return Response({'error': 'Exhibit not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)