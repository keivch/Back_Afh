from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import service, serializer
from django.http import HttpResponse
# Create your views here.


@swagger_auto_schema(
    method='post',
    operation_id='create_cost',
    operation_summary='Crear un nuevo costo',
    operation_description='Crea un nuevo costo asociado a una orden de trabajo con items específicos',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'work_order_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID de la orden de trabajo',
                example=1
            ),
            'items': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID del item/opción a asociar',
                example=5
            )
        },
        required=['work_order_id', 'items']
    ),
    responses={
        201: openapi.Response(
            description='Costo creado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Costo creado con éxito'
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Error en la petición',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='error en la petición'
                    )
                }
            )
        )
    },
    tags=['Costos']
)
@api_view(['POST'])
def add_view(request):
    data = request.data
    try:
        work_order_id = data.get('work_order_id')
        items = data.get('items')
        cost = service.create(work_order_id, items)
        if cost:
            return Response({'message': 'Costo creado con éxito'}, 201)
        else:
            return Response({'error': 'error en la petición'}, 400)
    except Exception as e:
        return Response({'error': str(e)})


@swagger_auto_schema(
    method='get',
    operation_id='get_cost',
    operation_summary='Obtener un costo específico',
    operation_description='Obtiene los detalles de un costo específico por su ID',
    manual_parameters=[
        openapi.Parameter(
            'cost_id',
            openapi.IN_PATH,
            description='ID del costo a obtener',
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    responses={
        200: openapi.Response(
            description='Costo encontrado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='ID del costo',
                        example=1
                    ),
                    'items': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Detalles del item/opción asociado'
                    ),
                    'work_order': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Detalles de la orden de trabajo'
                    ),
                    'total_value': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description='Valor total del costo',
                        example=150000.0
                    ),
                    'get_total_value_formatted': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Valor total formateado como moneda (campo calculado)',
                        example='$150.000'
                    )
                }
            )
        ),
        404: openapi.Response(
            description='Costo no encontrado',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Costo no encontrado'
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Error en la petición',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Error al procesar la petición'
                    )
                }
            )
        )
    },
    tags=['Costos']
)
@api_view(['GET'])
def get_view(request, cost_id):
    try:
        cost = service.get(cost_id)
        if cost:
            data = serializer.CostsSerializer(cost).data
            return Response(data, 200)
        else:
            return Response({'error': 'Costo no encontrado'}, 404)
    except Exception as e:
        return Response({'error': str(e)}, 400)

@swagger_auto_schema(
    method='patch',
    operation_id='update_cost',
    operation_summary='Actualizar un costo existente',
    operation_description='Actualiza los datos de un costo existente. Solo se actualizan los campos proporcionados.',
    manual_parameters=[
        openapi.Parameter(
            'cost_id',
            openapi.IN_PATH,
            description='ID del costo a actualizar',
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'work_order_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID de la orden de trabajo (opcional)',
                example=2
            ),
            'items': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID del item/opción a asociar (opcional)',
                example=7
            )
        }
    ),
    responses={
        200: openapi.Response(
            description='Costo actualizado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Costo actualizado con éxito'
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Error al actualizar el costo',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='No se pudo actualizar el costo'
                    )
                }
            )
        )
    },
    tags=['Costos']
)
@api_view(['PATCH'])
def update_view(request, cost_id):
    data = request.data
    work_order_id = data.get('work_order_id', None)
    items = data.get('items', None)
    try:
        cost = service.update(cost_id, work_order_id, items)
        if cost:
            return Response({'message': 'Costo actualizado con éxito'}, 200)
        else:
            return Response({'error': 'No se pudo actualizar el costo'}, 400)
    except Exception as e:
        return Response({'error': str(e)}, 400)

@swagger_auto_schema(
    method='delete',
    operation_id='delete_cost',
    operation_summary='Eliminar un costo',
    operation_description='Elimina permanentemente un costo del sistema',
    manual_parameters=[
        openapi.Parameter(
            'cost_id',
            openapi.IN_PATH,
            description='ID del costo a eliminar',
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    responses={
        200: openapi.Response(
            description='Costo eliminado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Costo eliminado con éxito'
                    )
                }
            )
        ),
        404: openapi.Response(
            description='Costo no encontrado',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Costo no encontrado'
                    )
                }
            )
        ),
        400: openapi.Response(
            description='Error al eliminar el costo',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Error al procesar la eliminación'
                    )
                }
            )
        )
    },
    tags=['Costos']
)
@api_view(['DELETE'])
def delete_view(request, cost_id):
    try:
        result = service.delete(cost_id)
        if result:
            return Response({'message': 'Costo eliminado con éxito'}, 200)
        else:
            return Response({'error': 'Costo no encontrado'}, 404)
    except Exception as e:
        return Response({'error': str(e)}, 400)

@swagger_auto_schema(
    method='get',
    operation_id='list_all_costs',
    operation_summary='Listar todos los costos',
    operation_description='Obtiene una lista de todos los costos registrados en el sistema',
    responses={
        200: openapi.Response(
            description='Lista de costos obtenida exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID del costo',
                            example=1
                        ),
                        'items': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description='Detalles del item/opción asociado'
                        ),
                        'work_order': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description='Detalles de la orden de trabajo'
                        ),
                        'total_value': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description='Valor total del costo',
                            example=150000.0
                        ),
                        'get_total_value_formatted': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Valor total formateado como moneda (campo calculado)',
                            example='$150.000'
                        )
                    }
                )
            )
        ),
        400: openapi.Response(
            description='Error al obtener la lista de costos',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example='Error al procesar la petición'
                    )
                }
            )
        )
    },
    tags=['Costos']
)
@api_view(['GET'])
def list_all_view(request):
    try:
        costs = service.list_all()
        data = serializer.CostsSerializer(costs, many=True).data
        return Response(data, 200)
    except Exception as e:
        return Response({'error': str(e)}, 400)

@api_view(['GET'])
def generate_pdf_view(request, cost_id):
    try:
        pdf = service.generate_pdf(cost_id)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Costos.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, 400)
