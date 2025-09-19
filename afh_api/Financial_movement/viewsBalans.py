from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .service import get_balance, get_by_method_of_paymenth, get_monthly_balans, generate_financial_report_pdf
from .models import FinancialMovement



@api_view(['GET'])
def get_balance_view(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        account_id = request.GET.get('account_id')
        if account_id is not None and account_id != "":
            try:
                account_id = int(account_id)
            except ValueError:
                return Response({'error': 'account_id debe ser un entero'}, status=400)
        else:
            account_id = None

        result =  get_balance(start_date=start, end_date=end, account_id=account_id)
        return Response(result, status=200)
    except Exception as e:
        return Response({'error': str(e)}, 500)
    
@api_view(['GET'])
def get_by_method_of_paymenth_view(request, option):
    try:
        account_id = request.GET.get('account_id')
        if account_id is not None and account_id != "":
            try:
                account_id = int(account_id)
            except ValueError:
                return Response({'error': 'account_id debe ser un entero'}, status=400)
        else:
            account_id = None

        incomes = get_by_method_of_paymenth(option=option, account_id=account_id)
        return Response(incomes, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_balans_by_month_view(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        account_id = request.GET.get('account_id')
        if account_id is not None and account_id != "":
            try:
                account_id = int(account_id)
            except ValueError:
                return Response({'error': 'account_id debe ser un entero'}, 400)
        else:
            account_id = None

        balans = get_monthly_balans(start=start, end=end, account_id=account_id)
        return Response(balans, status=200)
    except Exception as e:
        return Response({'error': str(e)}, 500)

@api_view(['GET'])
def get_balans_pdf(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        account_id = request.GET.get('account_id')
        if account_id is not None and account_id != "":
            try:
                account_id = int(account_id)
            except ValueError:
                return Response({'error': 'account_id debe ser un entero'}, 400)
        else:
            account_id = None
        if not start or not end:
            return Response({'error': 'todos los datos son necesarios'}, 400)
        buffer = generate_financial_report_pdf(start_date=start, end_date=end, account_id=account_id)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_financiero.pdf"'
        return response
    except Exception as e:
        return Response({'error': str(e)}, 500)


