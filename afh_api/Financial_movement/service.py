from .models import Egress, Income
import cloudinary
import cloudinary.uploader
from decimal import Decimal
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import TruncMonth
import calendar
from datetime import datetime
from django.template.loader import render_to_string, get_template
import weasyprint
from io import BytesIO


def upload_image(imagefield):
    if not imagefield:
        return None
    valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if imagefield.content_type not in valid_image_types:
        raise ValueError('Formato de imagen no válido. Solo se permiten JPEG, PNG, GIF o WEBP.')
    imagefield.seek(0)
    result = cloudinary.uploader.upload(imagefield, folder="afhimages/")
    return result['secure_url']

def create_egress(responsible, amount, date, reason, payment_method,  origin_account,  observations = None, voucher = None):
    try:
        amount = Decimal(amount)
        
        new_egress = Egress.objects.create(
            responsible = responsible,
            amount = amount,
            date = date,
            reason = reason,
            payment_method = payment_method, 
            origin_account = origin_account
        )

        if voucher:
            url = upload_image(voucher)
            new_egress.voucher = url
        if observations:
            new_egress.observations = observations
        new_egress.save()
        
        return new_egress
    except Exception as e:
        raise e
    

def update_egress(id, responsible = None, date = None , reason = None, payment_method = None, observations = None, origin_account = None, voucher = None):
    try:
        egress = Egress.objects.get(id=id)

        if responsible:
            egress.responsible = responsible
        if date:
            egress.date = date
        if reason:
            egress.reason = reason
        if payment_method:
            egress.payment_method = payment_method
        if observations:
            egress.observations = observations
        if origin_account:
            egress.origin_account = origin_account
        if voucher:
            url = upload_image(voucher)
            egress.voucher = url
        
        egress.save()
    except Exception as e:
        raise e
    
def create_income(responsible, amount, date, reason,  destination_account, payment_method, observations = None, voucher = None):
    try:
        amount = Decimal(amount)

        new_income = Income.objects.create(
            responsible = responsible,
            amount = amount,
            date = date,
            reason = reason,
            payment_method = payment_method,
            destination_account = destination_account
        )

        if voucher:
            url = upload_image(voucher)
            new_income.voucher = url
        if observations:
            new_income.observations = observations
        new_income.save()

        return new_income
    except Exception as e:
        raise e

def update_income(id, responsible = None, date = None, reason = None, payment_method = None, observations = None, voucher = None,destination_account = None):
    try:
        
        income = Income.objects.get(id=id)

        if responsible:
            income.responsible = responsible
        if date:
            income.date = date
        if reason:
            income.reason = reason
        if payment_method:
            income.payment_method = payment_method
        if observations:
            income.observations = observations
        if voucher:
            url = upload_image(voucher)
            income.voucher = url
        if destination_account:
            income.destination_account = destination_account
        
        income.save()
    except Exception as e:
        raise e
    
def get_incomes():
    try:
        incomes = Income.objects.all()
        return incomes
    except Exception as e:
        return str(e)
    
def get_income_by_id(id):
    try:
        income = Income.objects.get(id=id)
        return income
    except Exception as e:
        return str(e)
    
def get_egress():
    try:
        egress = Egress.objects.all()
        return egress
    except Exception as e:
        return str(e)
    
def get_egress_by_id(id):

    try:
        egress = Egress.objects.get(id=id)
        return egress
    except Exception as e:
        return str(e)
    

def get_balance(start_date=None, end_date=None):
    filters = {}
    if start_date and end_date:
        filters['date__range'] = (start_date, end_date)

    total_incomes = Income.objects.filter(**filters).aggregate(total=Sum('amount'))['total'] or 0
    total_egress = Egress.objects.filter(**filters).aggregate(total=Sum('amount'))['total'] or 0

    return {
        'ingresos': total_incomes,
        'egresos': total_egress,
        'balance': total_incomes - total_egress
    }

def get_by_method_of_paymenth(option):
    if option == 1:
        return Income.objects.values('payment_method').annotate(total=Sum('amount'), cantidad=Count('id'))
    if option == 2:
        return Egress.objects.values('origin_account').annotate(total=Sum('amount'), cantidad=Count('id'))
    
def get_monthly_balans(start, end):
    try:
        filters = {}
        if start and end:
            filters['date__range'] = (start, end)

        # Agrupar ingresos por mes
        ingresos_mensuales = (
            Income.objects.filter(**filters)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        # Agrupar egresos por mes
        egresos_mensuales = (
            Egress.objects.filter(**filters)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        # Convertir a diccionarios para fácil acceso
        ingresos_dict = {i['month'].strftime('%Y-%m'): i['total'] for i in ingresos_mensuales}
        egresos_dict = {e['month'].strftime('%Y-%m'): e['total'] for e in egresos_mensuales}

        # Unificar los meses
        meses = sorted(set(ingresos_dict.keys()) | set(egresos_dict.keys()))

        resultado = []
        for mes in meses:
            anio, mes_num = mes.split('-')
            nombre_mes = calendar.month_name[int(mes_num)]
            ingresos = ingresos_dict.get(mes, 0)
            egresos = egresos_dict.get(mes, 0)
            resultado.append({
                "mes": nombre_mes,
                "ingresos": ingresos,
                "egresos": egresos,
                "balance": ingresos - egresos
            })
        return resultado
    except Exception as e:
        raise e
    

def generate_financial_report_pdf(start_date, end_date):
    """
    Genera un reporte financiero en PDF usando WeasyPrint y template HTML.
    
    Args:
        start_date (str or datetime): Fecha de inicio en formato 'YYYY-MM-DD'
        end_date (str or datetime): Fecha de fin en formato 'YYYY-MM-DD'
        company_name (str): Nombre de la empresa para el encabezado
    
    Returns:
        HttpResponse: Respuesta HTTP con el PDF generado
    """
    try:
        # Convertir fechas a datetime si son strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # 1. Obtener balance general usando tu método
        balance_data = get_balance(start_date, end_date)
        
        # 2. Obtener ingresos por método de pago
        income_methods_raw = get_by_method_of_paymenth(1)
        income_methods = []
        total_income = balance_data['ingresos']
        
        for method in income_methods_raw:
            total_monto = method['total']
            if isinstance(total_monto, list):
                total_monto = total_monto[0] if total_monto else 0

            income_methods.append({
                'payment_method': method.get('payment_method') or 'No especificado',
                'cantidad': method.get('cantidad', 0),
                'total': total_monto,
                'porcentaje': round((total_monto / total_income * 100), 2) if total_income > 0 else 0
            })
        
        # 3. Obtener egresos por cuenta de origen
        expense_accounts_raw = get_by_method_of_paymenth(2)
        expense_accounts = []
        total_expense = balance_data['egresos']
        
        for account in expense_accounts_raw:
            expense_accounts.append({
                'origin_account': account['origin_account'] or 'No especificado',
                'cantidad': account['cantidad'],
                'total': account['total'],
                'porcentaje': round((account['total'] / total_expense * 100), 2) if total_expense > 0 else 0
            })
        
        # 4. Obtener balance mensual
        monthly_balance = get_monthly_balans(start_date, end_date)
        
        # 5. Calcular estadísticas adicionales
        stats = calculate_additional_stats(monthly_balance)

        template = get_template('balans.html')
        
        # 6. Preparar contexto para el template
        html = template.render ({
            'company_name': 'AFH METALMECANICO',
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y'),
            'generation_date': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'balance_data': balance_data,
            'income_methods': income_methods,
            'expense_accounts': expense_accounts,
            'monthly_balance': monthly_balance,
            'stats': stats,
            'has_income_methods': len(income_methods) > 0,
            'has_expense_accounts': len(expense_accounts) > 0,
            'has_monthly_data': len(monthly_balance) > 0,
        })
        
        buffer = BytesIO()
        weasyprint.HTML(string=html).write_pdf(buffer)
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        print(f"Error generating financial report PDF: {e}")
        raise e
    
def calculate_additional_stats(monthly_balance):
    """
    Calcula estadísticas adicionales para el reporte.
    """
    try:
        stats = {
            'total_months': len(monthly_balance),
            'positive_months': len([m for m in monthly_balance if m['balance'] > 0]),
            'negative_months': len([m for m in monthly_balance if m['balance'] < 0]),
            'best_month': None,
            'worst_month': None,
            'avg_monthly_income': 0,
            'avg_monthly_expense': 0,
            'max_monthly_amount': 0,
        }
        
        if monthly_balance:
            # Mejor y peor mes
            stats['best_month'] = max(monthly_balance, key=lambda x: x['balance'])
            stats['worst_month'] = min(monthly_balance, key=lambda x: x['balance'])
            
            # Promedios mensuales
            stats['avg_monthly_income'] = sum(m['ingresos'] for m in monthly_balance) / len(monthly_balance)
            stats['avg_monthly_expense'] = sum(m['egresos'] for m in monthly_balance) / len(monthly_balance)
            
            # Máximo para los gráficos
            stats['max_monthly_amount'] = max(
                max(m['ingresos'] for m in monthly_balance),
                max(m['egresos'] for m in monthly_balance)
            )
        
        return stats
    except Exception as e:
        print(f"Error calculating additional stats: {e}")
        raise e
