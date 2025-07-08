from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .service import get_balance, get_by_method_of_paymenth, get_monthly_balans
from .models import FinancialMovement



@api_view(['GET'])
def get_balance_view(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        result =  get_balance(start_date=start, end_date=end)
        return Response(result, status=200)
    except Exception as e:
        return Response({'error': str(e)}, 500)
    
@api_view(['GET'])
def get_by_method_of_paymenth_view(request, option):
    try:
        incomes = get_by_method_of_paymenth(option=option)
        return Response(incomes, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_balans_by_month_view(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        balans = get_monthly_balans(start=start, end=end)
        return Response(balans, status=200)
    except Exception as e:
        return Response({'error': str(e)}, 500)


