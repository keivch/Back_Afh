from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .service import add_work_advance, get_work_advance, get_work_advance_by_id, delete_work_advance, edit_work_advance
from .models import WorkAdvance
from .serializer import WorkAdvanceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class WorkAdvanceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkAdvanceSerializer
    queryset = WorkAdvance.objects.all()


@swagger_auto_schema(
    method='post',
    operation_description="Crea un nuevo avance de trabajo.",
    manual_parameters=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['description'],
        properties={
            'exhibits_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date')
        },
    ),
    responses={
        201: openapi.Response(
            description="WorkAdvance creado exitosamente",
            examples={"application/json": {"message": "WorkAdvance created succesfully", "id": 1}}
        ),
        400: "Bad Request",
        500: "Internal Server Error"
    }
)

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
    

@swagger_auto_schema(
    method='patch',
    operation_description="Actualiza un avance de trabajo existente.",
    manual_parameters=[
        openapi.Parameter(
            'work_advance_id',
            openapi.IN_PATH,
            description="ID del avance de trabajo a actualizar",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[],
        properties={
            'exhibits_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                description="Lista de IDs de exhibits relacionados"
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Descripción del avance"
            ),
            'date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format='date',
                description="Fecha del avance (YYYY-MM-DD)"
            ),
        }
    ),
    responses={
        200: openapi.Response(
            description="Avance actualizado exitosamente",
            examples={"application/json": {"message": "update work advance succesfully"}}
        ),
        500: openapi.Response(
            description="Error interno del servidor",
            examples={"application/json": {"error": "detalle del error"}}
        )
    }
)
@api_view(['PATCH'])
def update_work_advance_view(request, work_advance_id):
    data = request.data
    try:
        exhibits_ids = data.get('exhibits_ids')
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
        works = get_work_advance()
        serializer = WorkAdvanceSerializer(works, many=True)
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