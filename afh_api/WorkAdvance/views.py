from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .service import add_work_advance, get_work_advance, get_work_advance_by_id, delete_work_advance, edit_work_advance
from .models import WorkAdvance
from .serializer import WorkAdvanceSerializer

# Create your views here.
class WorkAdvanceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkAdvanceSerializer
    queryset = WorkAdvance.objects.all()


@api_view(['POST'])
def add_work_advance_view(request):
    data = request.data
    try:
        exhibits_ids = data.get('exhibits_ids', [])
        description = data.get('description')
        date = data.get('date')
        if not description:
            return Response({'error': 'Description is required'}, status=400)
        work_advance = add_work_advance(exhibits_ids, description, date)
        return Response({'message:': 'WorkAdvance created succesfully', 'id': work_advance.id}, 201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PATCH'])
def update_work_advance_view(request, work_advance_id):
    data = request.data
    try:
        exhibits_ids = data.get('exhibits_ids', [])
        description = data.get('description')
        date = data.get('date')

        work = edit_work_advance(work_advance_id, exhibits_ids, description, date)
        return Response({'message': 'update work advance succesfully'}, 200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
def delete_work_order_view(request, work_advance_id):
    try:
        delete_work_advance(work_advance_id)
        return Response({'message': 'delete succesfully'}, 200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_work_advance_view(request):
    try:
        serializer = WorkAdvanceSerializer(many=True, data=get_work_advance())
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_work_advance_by_id_view(request, work_advance_id):
    try:
        work = get_work_advance_by_id(work_advance_id)
        serializer = WorkAdvanceSerializer(work)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)