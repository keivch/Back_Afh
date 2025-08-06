from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .service import add_advance_to_progress, remove_advance_from_progress, get_work_progress_by_id, get_all_work_progresses, change_work_progress_status, validate_customer, change_progress_percentage
from .models import WorkAdvance
from .serializer import WorkAdvanceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializer import WorkProgressSerializer


# Create your views here.
@swagger_auto_schema(
    method='put',
    operation_description="Asocia un avance de trabajo a un progreso de trabajo.",
    manual_parameters=[
        openapi.Parameter(
            'work_progress_id',
            openapi.IN_PATH,
            description="ID del progreso de trabajo",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            'work_advance_id',
            openapi.IN_PATH,
            description="ID del avance de trabajo",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Avance asociado exitosamente.",
            examples={"application/json": {"message": "Work advance added successfully."}}
        ),
        400: openapi.Response(
            description="Error en la solicitud.",
            examples={"application/json": {"error": "detalle del error"}}
        )
    }
)
@api_view(['PUT'])
def add_work_advance_view(request, work_progress_id, work_advance_id):
    try:
        add_advance_to_progress(work_progress_id=work_progress_id, work_advance_id=work_advance_id)
        return Response({"message": "Work advance added successfully."}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@swagger_auto_schema(
    method='put',
    operation_description="Desasocia un avance de trabajo de un progreso de trabajo.",
    manual_parameters=[
        openapi.Parameter(
            'work_progress_id',
            openapi.IN_PATH,
            description="ID del progreso de trabajo",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            'work_advance_id',
            openapi.IN_PATH,
            description="ID del avance de trabajo",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Avance desasociado exitosamente.",
            examples={"application/json": {"message": "Work advance removed successfully."}}
        ),
        400: openapi.Response(
            description="Error en la solicitud.",
            examples={"application/json": {"error": "detalle del error"}}
        )
    }
)    
@api_view(['PUT'])
def remove_work_advance_view(request, work_progress_id, work_advance_id):
    try:
        remove_advance_from_progress(work_progress_id=work_progress_id, work_advance_id=work_advance_id)
        return Response({"message": "Work advance removed successfully."}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
def get_work_progress_view(request, work_progress_id):
    try:
        work_progress = get_work_progress_by_id(work_progress_id)
        if work_progress:
            serializer = WorkProgressSerializer(work_progress)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "Work progress not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_all_work_progresses_view(request):
    try:
        work_progresses = get_all_work_progresses()
        serializer = WorkProgressSerializer(work_progresses, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@swagger_auto_schema(
    method='put',
    operation_description="Cambia el estado de un progreso de trabajo.",
    manual_parameters=[
        openapi.Parameter(
            'work_progress_id',
            openapi.IN_PATH,
            description="ID del progreso de trabajo",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['status'],
        properties={
            'status': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Nuevo estado del progreso de trabajo'
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="Estado actualizado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Datos actualizados del progreso de trabajo"
            )
        ),
        400: openapi.Response(
            description="Error en la solicitud.",
            examples={"application/json": {"error": "Status is required."}}
        ),
        404: openapi.Response(
            description="Progreso de trabajo no encontrado.",
            examples={"application/json": {"error": "Work progress not found."}}
        )
    }
)
@api_view(['PUT'])
def change_work_progress_status_view(request, work_progress_id):
    data = request.data
    try:
        new_status = data.get('status')
        if not new_status:
            return Response({"error": "Status is required."}, status=400)
        
        work_progress = change_work_progress_status(work_progress_id, new_status)
        if work_progress:
            return Response({'message': 'wor_progress updated succefully'}, status=200)
        else:
            return Response({"error": "Work progress not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['POST'])
def validate_customer_view(request):
    data = request.data
    try:
        code = data.get('code')
        email = data.get('email')
        if not code or not email:
            return Response({"error": "Code and email are required."}, status=400)
        
        work_order = validate_customer(code, email)
        if work_order:
            serializer = WorkProgressSerializer(work_order)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "Invalid code or email."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    


@swagger_auto_schema(
    method='put',
    operation_description="Actualiza el porcentaje de un progreso de trabajo existente.",
    manual_parameters=[
        openapi.Parameter(
            'work_progress_id',
            openapi.IN_PATH,
            description="ID del progreso de trabajo a actualizar",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['percentage'],
        properties={
            'percentage': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                format='integer',
                description='Nuevo valor del porcentaje de avance',
                example=85.0
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="Porcentaje actualizado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Porcentaje actualizado exitosamente'
                    )
                }
            )
        ),
        400: openapi.Response(
            description="Falta el campo 'percentage'.",
            examples={
                "application/json": {"error": "Debe enviar el porcentaje"}
            }
        ),
        500: openapi.Response(
            description="Error interno del servidor.",
            examples={
                "application/json": {"error": "Error inesperado"}
            }
        )
    }
)
@api_view(['PUT'])
def change_percentage_view(request, work_progress_id):
    data = request.data
    try:
        percentage = data.get('percentage')
        
        if not percentage:
            return Response({'error': 'Debe enviar el porcentaje'})
        change_progress_percentage(percentage, work_progress_id=work_progress_id)
        return Response({'message': 'Porcentaje actualizado exitosamente'}, 200)
    except Exception as e:
        return Response({'error': str(e)}, 500)