from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from rest_framework.views import APIView
from . import service
from .serializer import AccountSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

create_account_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['type', 'initial_amount', 'name'],
    properties={
        'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='1=Banco, 2=Caja'),
        'initial_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Monto inicial de la cuenta'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la cuenta'),
    },
)

update_account_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='1=Banco, 2=Caja'),
        'initial_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='(No editable actualmente)'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la cuenta'),
    },
)



@swagger_auto_schema(
    method='post',
    operation_summary='Crear cuenta',
    operation_description='Crea una nueva cuenta financiera (Banco/Caja).',
    request_body=create_account_request,
    responses={
        201: openapi.Response('Cuenta creada con éxito'),
        400: openapi.Response('Datos inválidos'),
        500: openapi.Response('Error del servidor')
    }
)
@api_view(['POST'])
def add_account_view(request):
    data = request.data
    try:
        type = data.get('type')
        initial_amount = data.get('initial_amount')
        name = data.get('name')

        if not type or not initial_amount or not name:
            return Response({'error': 'Todos los datos son requeridos'}, 400)

        new_account = service.create_account(type=type, initial_amount=initial_amount, name=name)

        return Response({'message': 'Cuenta creada con éxito'}, 201)
    except Exception as e:
        return Response({'error': str(e)}, 500)


@swagger_auto_schema(
    method='patch',
    operation_summary='Actualizar cuenta',
    operation_description='Actualiza una cuenta por su ID. Campos opcionales.',
    manual_parameters=[
        openapi.Parameter('id_account', openapi.IN_PATH, description='ID de la cuenta', type=openapi.TYPE_INTEGER),
    ],
    request_body=update_account_request,
    responses={
        200: openapi.Response('Cuenta actualizada con éxito'),
        500: openapi.Response('Error del servidor')
    }
)
@api_view(['PATCH'])
def update_account_view(request, id_account):
    data = request.data
    try:
        type = data.get('type')
        name = data.get('name')

        service.update_account(id_account, type, name)

        return Response({'message': 'Cuenta actualizada con éxito'}, 200)

    except Exception as e:
        return Response({'error': str(e)}, 500)
    


@swagger_auto_schema(
    method='get',
    operation_summary='Listar cuentas',
    operation_description='Retorna el listado de cuentas.',
    responses={
        200: AccountSerializer(many=True),
        500: openapi.Response('Error del servidor')
    }
)
@api_view(['GET'])
def get_accounts_view(request):
    try:
        accounts = service.get_accounts()
        serializer = AccountSerializer(accounts, many= True)
        return Response(serializer.data, 200)

    except Exception as e:
        return Response({'error': str(e)})


@swagger_auto_schema(
    method='get',
    operation_summary='Obtener cuenta',
    operation_description='Retorna el detalle de una cuenta por ID.',
    manual_parameters=[
        openapi.Parameter('id_account', openapi.IN_PATH, description='ID de la cuenta', type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: AccountSerializer(),
        500: openapi.Response('Error del servidor')
    }
)
@api_view(['GET'])
def get_account_view(request, id_account):
    try:
        account = service.get_account(id_account)
        serializer = AccountSerializer(account)
        return Response(serializer.data, 200)
    
    except Exception as e:
        return Response({'error': str(e)}, 500)

    
