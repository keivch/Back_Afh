from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import Egress
from .serializer import EgressSerializer
from .service import create_egress, update_egress, get_egress_by_id, get_egress
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EgressViewSet(viewsets.ModelViewSet):
    serializer_class = EgressSerializer
    queryset = Egress.objects.all()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_egrees_view(request):
    data = request.data
    try:
        responsible = data.get('responsible')
        amount = data.get('amount')
        date = data.get('date')
        reason = data.get('reason')
        payment_method = data.get('payment_method')
        observations = data.get('observations')
        voucher = request.FILES.get('voucher')
        origin_account = data.get('origin_account')

        if not responsible or not amount or not date or not reason or not payment_method or not origin_account:
            return Response({'Error': 'Todos los datos son requeridos'}, 400)

        egress = create_egress(responsible=responsible, amount= amount, date= date, reason= reason, payment_method=payment_method, observations=observations,
                      voucher= voucher, origin_account=origin_account)

        return Response({'message': 'Creado con exito', 'id': egress.id}, 201)
    except Exception as e:
        return Response({'Error': str(e)}, 500)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_egress_view(request, egress_id):
    data = request.data
    try:
        responsible = data.get('responsible')
        date = data.get('date')
        reason = data.get('reason')
        payment_method = data.get('payment_method')
        observations = data.get('observations')
        voucher = request.FILES.get('voucher')
        origin_account = data.get('origin_account')

        update_egress( id=egress_id ,responsible=responsible, date= date, reason= reason, payment_method=payment_method, observations=observations,
                      voucher= voucher, origin_account=origin_account)

        return Response({'message': 'Actualizado con exito'}, 200)
    except Exception as e:
        return Response({'Error': str(e)}, 500)
    
@api_view(['GET'])
def get_eggress_view(request):
    try:
        egress = get_egress()
        serializer =  EgressSerializer(egress, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)})
    
@api_view(['GET'])
def get_egress_by_id_view(request, egress_id):
    try:
        egress = get_egress_by_id(egress_id)
        serializer = EgressSerializer(egress)
        return Response({serializer.data}, status=200)
    except Exception as e:
        return Response({'error': str(e)})
