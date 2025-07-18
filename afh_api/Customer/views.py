from .services import create_customer, update_customer, delete_customer, get_customers, get_customer_by_id
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .Serializer import CustomerSerializer
from .models import Customer

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_customer(request):
    data = request.data
    try:
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        post = data.get('post')
        representative = data.get('representative')

        if not name or not email or not phone or not post or not representative:
            return Response({'error': 'All fields are required'}, status=400)
        
        create_customer(name, email, phone, post, representative)
        return Response({'message': 'Cliente creado exitosamente'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer_view(request, customer_id):
    data = request.data
    try:
        name  = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        post = data.get('post')
        representative = data.get('representative')

        if not name:
            name = None
        if not email:
            email = None
        if not phone:
            phone = None
        if not post:
            post = None
        update_customer(customer_id, name, email, phone, post,representative)
        return Response({'message': 'Cliente actualizado exitosamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_customer_view(request, customer_id):
    try:
        delete_customer(customer_id)
        if delete_customer(customer_id) is False:
            return Response({'error': 'El cliente esta asociado a una cotizacion, no se puede eliminar'}, status=400)
        return Response({'message': 'Cliente eliminado exitosamente'}, status=204)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
def get_customers_view(request):
    try:
        customers = get_customers()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_customer_by_id_view(request, customer_id):
    try:
        customer = get_customer_by_id(customer_id)
        if customer is None:
            return Response({'error': 'Customer not found'}, status=404)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)