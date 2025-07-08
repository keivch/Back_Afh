from .models import Egress, Income
import cloudinary
import cloudinary.uploader
from decimal import Decimal
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import TruncMonth
import calendar


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
        print("Error al crear el egreso:", str(e))
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
        print("Error el egreso:", str(e))
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
        print("Error el egreso:", str(e))
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
        print("Error el egreso:", str(e))
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
            año, mes_num = mes.split('-')
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
