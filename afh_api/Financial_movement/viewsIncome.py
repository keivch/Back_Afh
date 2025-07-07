from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import Income
from .serializer import IncomeSerializer
from .service import create_income, update_income, get_income_by_id, get_incomes

# Create your views here.
class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()


@api_view(['POST'])
def create_income_view(request):
    data = request.data
    try:
        responsible = data.get('responsible')
        amount = data.get('amount')
        date = data.get('date')
        reason = data.get('reason')
        payment_method = data.get('payment_method')
        observations = request.FILES.get('observations')
        voucher = data.get('voucher')
        destination_account = data.get('destination_account')

        if not responsible or not date or not reason or not payment_method or not destination_account or not amount:
            return Response({'Error': 'Todos lso campos son requeridos'}, 400)
        
        new_income = create_income(responsible=responsible, amount=amount, date=date, reason=reason, payment_method=payment_method, observations=observations, voucher=voucher,
                      destination_account=destination_account)
        
        return Response({'message': 'Creado con exito', "id": new_income.id }, 201)
    except Exception as e:
        return Response({'Error': str(e)})

@api_view(['PATCH'])
def update_income_view(request, income_id):
    data = request.data
    try:
        responsible = data.get('responsible')
        date = data.get('date')
        reason = data.get('reason')
        payment_method = data.get('payment_method')
        observations = request.FILES.get('observations')
        voucher = data.get('voucher')
        destination_account = data.get('destination_account')

        update_income(id=income_id, responsible=responsible, date=date, reason=reason, payment_method=payment_method,
                      observations=observations, voucher=voucher, destination_account=destination_account)
        
        return Response({'message': 'actualizado con exito'}, 200)
    except Exception as e:
        return Response({'error': str(e)}, 500)
    
@api_view(['GET'])
def get_incomes_view(request):
    try:
        incomes = get_incomes()
        serializer =  IncomeSerializer(incomes, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({'error': str(e)})
    
@api_view(['GET'])
def get_income_by_id_view(request, income_id):
    try:
        income = get_income_by_id(income_id)
        serializer = IncomeSerializer(income)
        return Response({serializer.data}, status=200)
    except Exception as e:
        return Response({'error': str(e)})


