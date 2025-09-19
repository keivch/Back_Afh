from django.http import HttpResponse
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
            ),
            'user_email': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description='Email del usuario que entrega la herramienta para mantenimiento'
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
        user_email = data.get('user_email')
    
        new_maintenance = service.create(maintenance_technician_name, tool_id, date, maintenance_days, observations, next_maintenance_date, type, user_email)

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
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del mantenimiento'),
                        'maintenance_technician_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del técnico encargado del mantenimiento'),
                        'tool': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description='Información de la herramienta',
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la herramienta'),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la herramienta'),
                                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Código de la herramienta'),
                                'state': openapi.Schema(type=openapi.TYPE_INTEGER, description='Estado de la herramienta: 1=Activa, 2=Inactiva, 3=En uso, 4=Reservada, 5=En mantenimiento'),
                                'image': openapi.Schema(type=openapi.TYPE_STRING, description='URL de la imagen de la herramienta'),
                                'marca': openapi.Schema(type=openapi.TYPE_STRING, description='Marca de la herramienta')
                            }
                        ),
                        'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha del mantenimiento'),
                        'maintenance_days': openapi.Schema(type=openapi.TYPE_INTEGER, description='Días de mantenimiento'),
                        'observations': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones'),
                        'next_maintenance_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Próxima fecha de mantenimiento'),
                        'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tipo de mantenimiento: 1=Correctivo, 2=Preventivo'),
                        'user_delivery': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description='Información del usuario que entrega la herramienta',
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
                                'role': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rol del usuario: 1=ADMIN, 2=NO ADMIN'),
                                'user': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description='Información del usuario de Django',
                                    properties={
                                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
                                        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre'),
                                        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido'),
                                        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email del usuario')
                                    }
                                )
                            }
                        ),
                        'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de entrega calculada (fecha + días de mantenimiento)')
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
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del mantenimiento'),
                    'maintenance_technician_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del técnico encargado del mantenimiento'),
                    'tool': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Información de la herramienta',
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la herramienta'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la herramienta'),
                            'code': openapi.Schema(type=openapi.TYPE_STRING, description='Código de la herramienta'),
                            'state': openapi.Schema(type=openapi.TYPE_INTEGER, description='Estado de la herramienta: 1=Activa, 2=Inactiva, 3=En uso, 4=Reservada, 5=En mantenimiento'),
                            'image': openapi.Schema(type=openapi.TYPE_STRING, description='URL de la imagen de la herramienta'),
                            'marca': openapi.Schema(type=openapi.TYPE_STRING, description='Marca de la herramienta')
                        }
                    ),
                    'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha del mantenimiento'),
                    'maintenance_days': openapi.Schema(type=openapi.TYPE_INTEGER, description='Días de mantenimiento'),
                    'observations': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones'),
                    'next_maintenance_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Próxima fecha de mantenimiento'),
                    'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tipo de mantenimiento: 1=Correctivo, 2=Preventivo'),
                    'user_delivery': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Información del usuario que entrega la herramienta',
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
                            'role': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rol del usuario: 1=ADMIN, 2=NO ADMIN'),
                            'user': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='Información del usuario de Django',
                                properties={
                                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
                                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre'),
                                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido'),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email del usuario')
                                }
                            )
                        }
                    ),
                    'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de entrega calculada (fecha + días de mantenimiento)')
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

@swagger_auto_schema(
    method='get',
    operation_summary="Generar PDF del ticket de mantenimiento",
    operation_description="Genera y descarga un PDF del ticket de entrega de herramienta a mantenimiento",
    manual_parameters=[
        openapi.Parameter(
            'maintenance_id',
            openapi.IN_PATH,
            description="ID del mantenimiento para generar el PDF",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='PDF generado exitosamente',
            content={
                'application/pdf': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        ),
        400: openapi.Response(
            description='Error en la solicitud',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='id del mantenimiento es requerido')
                }
            )
        ),
        404: openapi.Response(
            description='Mantenimiento no encontrado',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Mantenimiento con ID 123 no encontrado')
                }
            )
        ),
        500: openapi.Response(
            description='Error interno del servidor',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, example='Error generando PDF: [detalle del error]')
                }
            )
        )
    }
)
@api_view(['GET'])
def get_pdf(request, maintenance_id):
    try:
        if not maintenance_id:
            return Response({'error': 'id del mantenimiento es requerido'}, 400)
        buffer = service.get_pdf(maintenance_id)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Ticket-{maintenance_id}.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@swagger_auto_schema(
    method='put',
    operation_summary="Finalizar mantenimiento",
    operation_description="Finaliza un mantenimiento específico",
    manual_parameters=[
        openapi.Parameter(
            'maintenance_id',
            openapi.IN_PATH,
            description="ID del mantenimiento a finalizar",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Mantenimiento finalizado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example='Mantenimiento finalizado con éxito')
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
@api_view(['PUT'])
def end_maintenance_view(request, maintenance_id):
    try:
        service.end_maintenance(maintenance_id)
        return Response({'message': 'Mantenimiento finalizado con éxito'}, 200)
    except Exception as e:
        return Response({'error': str(e)}, 500)