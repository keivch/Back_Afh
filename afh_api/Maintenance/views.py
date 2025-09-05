from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import service
from .serializer import MaintenanceSerializer
# Create your views here.

@swagger_auto_schema(
    method='post',
    operation_summary="Crear nuevo mantenimiento",
    operation_description="Crea un nuevo registro de mantenimiento para una herramienta específica",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['maintenance_technician_name', 'tool_id', 'maintenance_days', 'next_maintenance_date'],
        properties={
            'maintenance_technician_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Nombre del técnico encargado del mantenimiento',
                max_length=700
            ),
            'tool_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID de la herramienta a la que se le realizará el mantenimiento'
            ),
            'date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Fecha del mantenimiento (formato: YYYY-MM-DD)'
            ),
            'maintenance_days': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Número de días que durará el mantenimiento'
            ),
            'observations': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Observaciones adicionales sobre el mantenimiento'
            ),
            'next_maintenance_date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Fecha programada para el próximo mantenimiento (formato: YYYY-MM-DD)'
            ),
            'type': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Tipo de mantenimiento: 1=Correctivo, 2=Preventivo',
                enum=[1, 2],
                default=1
            )
        }
    ),
    responses={
        201: openapi.Response(
            description='Mantenimiento creado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example='Nuevo mantenimiento agendado con éxito')
                }
            )
        ),
        400: openapi.Response(
            description='Error en la solicitud',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='error agendando el mantenimiento')
                }
            )
        ),
        500: openapi.Response(
            description='Error interno del servidor',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Error interno del servidor')
                }
            )
        )
    }
)
@api_view(['POST'])
def add_maintenance_view(request):
    try:
        data = request.data

        maintenance_technician_name = data.get('maintenance_technician_name')
        tool_id = data.get('tool_id')
        date = data.get('date')
        maintenance_days = data.get('maintenance_days')
        observations = data.get('observations')
        next_maintenance_date = data.get('next_maintenance_date')
        type = data.get('type')
    
        new_maintenance = service.create(maintenance_technician_name, tool_id, date, maintenance_days, observations, next_maintenance_date, type)

        if new_maintenance:
            return Response({'message': 'Nuevo mantenimiento agendado con éxito'}, 201)
        else:
            return Response({'error': 'error agendando el mantenimiento'}, 400)
    except Exception as e:
        return Response({'error': str(e)}, 500)

@swagger_auto_schema(
    method='patch',
    operation_summary="Actualizar mantenimiento",
    operation_description="Actualiza un registro de mantenimiento existente",
    manual_parameters=[
        openapi.Parameter(
            'maintenance_id',
            openapi.IN_PATH,
            description="ID del mantenimiento a actualizar",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'maintenance_technician_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Nombre del técnico encargado del mantenimiento',
                max_length=700
            ),
            'tool_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID de la herramienta a la que se le realizará el mantenimiento'
            ),
            'date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Fecha del mantenimiento (formato: YYYY-MM-DD)'
            ),
            'maintenance_days': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Número de días que durará el mantenimiento'
            ),
            'observations': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Observaciones adicionales sobre el mantenimiento'
            ),
            'next_maintenance_date': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Fecha programada para el próximo mantenimiento (formato: YYYY-MM-DD)'
            ),
            'type': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Tipo de mantenimiento: 1=Correctivo, 2=Preventivo',
                enum=[1, 2]
            )
        }
    ),
    responses={
        200: openapi.Response(
            description='Mantenimiento actualizado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example='Mantenimiento actualizado con éxito')
                }
            )
        ),
        500: openapi.Response(
            description='Error interno del servidor',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Error interno del servidor')
                }
            )
        )
    }
)
@api_view(['PATCH'])
def update_maintenance_view(request, maintenance_id):
    try:
        data = request.data
        maintenance_technician_name = data.get('maintenance_technician_name')
        tool_id = data.get('tool_id')
        date = data.get('date')
        maintenance_days = data.get('maintenance_days')
        observations = data.get('observations')
        next_maintenance_date = data.get('next_maintenance_date')
        type = data.get('type')
        
        service.update_maintenance(maintenance_id, maintenance_technician_name, tool_id, maintenance_days, observations, next_maintenance_date, date, type)
        return Response({'message': 'Mantenimiento actualizado con éxito'}, 200)
    except Exception as e:
        return Response({'error': str(e)}, 500)

@swagger_auto_schema(
    method='get',
    operation_summary="Obtener todos los mantenimientos",
    operation_description="Obtiene una lista de todos los mantenimientos registrados",
    responses={
        200: openapi.Response(
            description='Lista de mantenimientos obtenida exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del mantenimiento'),
                        'maintenance_technician_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del técnico'),
                        'tool': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description='Información de la herramienta',
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'state': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        ),
                        'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha del mantenimiento'),
                        'maintenance_days': openapi.Schema(type=openapi.TYPE_INTEGER, description='Días de mantenimiento'),
                        'observations': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones'),
                        'next_maintenance_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Próxima fecha de mantenimiento'),
                        'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tipo de mantenimiento: 1=Correctivo, 2=Preventivo')
                    }
                )
            )
        ),
        500: openapi.Response(
            description='Error interno del servidor',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Error interno del servidor')
                }
            )
        )
    }
)
@api_view(['GET'])
def get_all_maintenances(request):
    try:
        maintenances = service.get_maintenances()
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response(serializer.data, 200)
    except Exception as e:
        return Response({'error': str(e)}, 500)

@swagger_auto_schema(
    method='get',
    operation_summary="Obtener mantenimiento por ID",
    operation_description="Obtiene un mantenimiento específico por su ID",
    manual_parameters=[
        openapi.Parameter(
            'maintenance_id',
            openapi.IN_PATH,
            description="ID del mantenimiento a obtener",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Mantenimiento obtenido exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del mantenimiento'),
                    'maintenance_technician_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del técnico'),
                    'tool': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Información de la herramienta',
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'state': openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    ),
                    'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha del mantenimiento'),
                    'maintenance_days': openapi.Schema(type=openapi.TYPE_INTEGER, description='Días de mantenimiento'),
                    'observations': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones'),
                    'next_maintenance_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Próxima fecha de mantenimiento'),
                    'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tipo de mantenimiento: 1=Correctivo, 2=Preventivo')
                }
            )
        ),
        500: openapi.Response(
            description='Error interno del servidor',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Error interno del servidor')
                }
            )
        )
    }
)
@api_view(['GET'])
def get_maintenance_by_id(request, maintenance_id):
    try:
        maintenance = service.get_maintenance_id(maintenance_id)
        serializer = MaintenanceSerializer(maintenance)
        return Response(serializer.data, 200)
    except Exception as e:
        return Response({'error': str(e)}, 500)
